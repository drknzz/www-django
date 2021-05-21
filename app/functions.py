from .models import User, Directory, File, SectionCategory, Status, StatusData, FileSection
from django.utils import timezone
import os
import subprocess

section_values = ["inv", "post-condition", "assert", "variant", "requires", "exits", "continues", "lemma", "ensures", "assigns", "check"]
status_values = ["Valid", "Invalid", "Unknown", "Timeout", "Proved", "Unchecked", "Counterexample", "Failed"]

#returns array of directories with child order
def dir_array(parent_dir, owner):
    dirs = Directory.objects.filter(parent_directory=parent_dir, availability=True, owner=owner.username)
    array = []
    for dir in dirs:
        array.append(dir)
        array = array + dir_array(dir, owner)
    return array


#adds to each directory in array its level
def dir_array_levels(dir_array):
    array = []
    for dir in dir_array:
        array.append([dir, range(dir.level)])
    return array


#returns array of arrays of files in order of directories from dir_array
def file_array(dir_array, owner):
    array = []
    for dir in dir_array:
        files = File.objects.filter(directory=dir[0], availability=True, owner=owner.username)
        array.append(files)
    return array


#merges list of dirs with list of files
def merge_dirs_files(dirs, files):
    for idx, dir in enumerate(dirs):
        dir.append(files[idx])
    return dirs


#returns list of dirs with their files
def get_dirs_and_files(owner):
    dirs = dir_array_levels(dir_array(None, owner))
    files = file_array(dirs, owner)
    return merge_dirs_files(dirs, files)


#recursively deletes directory
def delete_dir(dir):
    dir_files = File.objects.filter(directory=dir, availability=True)
    for file in dir_files:
        file.availability = False
        file.save()
    
    subdirs = Directory.objects.filter(parent_directory=dir, availability=True)
    for sdir in subdirs:
        delete_dir(sdir)

    dir.availability = False
    dir.save()


def get_result(file):
    path = file.file.path
    result_path = path[:path.rfind("/")] + "/result.txt"
    command = 'frama-c -wp -wp-log=r:"' + result_path + '" ' + path

    os.system(command)

    result = subprocess.run(
        ['cat', result_path],
        stdout=subprocess.PIPE,
        encoding="utf-8"
    )
    return result.stdout


def create_sections(file):
    with open(file.file.path, 'r') as open_file:
        lines = list(open_file)
    open_file.close()

    section = False
    begin = end = 1
    keyword = ''

    for idx, line in enumerate(lines):
        if section == False and (line.find("/*@") != -1 or line.find("//@") != -1 or line.find("@") != -1) and line.find("@*/") == -1:
            begin = idx + 1
            section = True
            words = line.split()
            if words[1] == "loop":
                keyword = line.split()[2]
            else:
                keyword = line.split()[1]
        if section == True and line.find(";") != -1:
            end = idx + 1
            section = False
            section_category = SectionCategory(category=keyword, last_updated=timezone.now(), validity=True)
            section_category.save()

            file_section = FileSection(name=keyword, category=section_category, file=file, begin=begin, end=end)
            file_section.save()


def get_command(file_name, rte, prover, vcs):
    file_obj = File.objects.get(name=file_name)

    result = "frama-c -wp "

    if (prover != "None"):
        result += "-wp-prover " + prover + " "

    if vcs:
        result += '-wp-prop="'
        for vc in vcs:
            result += "-" + vc
        result += '" '

    if (rte == True):
        result += "-wp-rte "

    return result + file_obj.file.path


def basic_compile(file_name):
    file = File.objects.get(name=file_name)
    result = subprocess.run(
            ['frama-c', '-wp', '-wp-print', file.file.path],
            stdout=subprocess.PIPE,
            encoding="utf-8"
        )
    result = result.stdout

    divided_result = result.split("------------------------------------------------------------")

    del divided_result[0]
    return divided_result


def adv_compile(file_name, command):
    stream = os.popen(command)

    result = stream.read()
    divided_result = result.split("[wp]")

    return divided_result


def parse_compilation(compile_result, file_name, adv, owner):
    file = File.objects.get(name=file_name)
    sections = file.sections.all()
    result = []

    for idx, fragment in enumerate(compile_result):
        if idx == len(compile_result) - 1:
            if adv or compile_result[idx][0] != 'G':
                result.append(("", "", fragment, ""))
                break

        status = ""
        section = ""
        begin = ""

        for s in status_values:
            if s in fragment:
                status = s
                break

        for s in section_values:
            if s in fragment.lower():
                section = s
                break

        if section == "variant" and fragment[fragment.find("variant")-1] == 'n':
            section = "invariant"

        if section != "" and status != "":
            begin = create_status(section, status, fragment, sections, adv, owner)

        if section == "inv":
            section = "invariant"

        result.append((status, section, fragment, begin))
    
    return result


def create_status(section, status, fragment, sections, adv, owner):
    if adv:
        divid = fragment.split('_')
        try:
            if divid[-2].find(section) != -1 or divid[-1].find(section) != -1:
                num = 0
            elif divid[divid.index(section) + 1].isnumeric(): 
                num = int(divid[divid.index(section) + 1]) - 1  
            else:
                num = 0

            if section == "inv":
                section = "invariant"

            section_obj = sections.filter(name=section).order_by('pk')[num]
        except:
            return ""

        begin = getattr(section_obj, "begin")
    else:
        divid = fragment.split(' ')
        num = divid[divid.index("line") + 1]

        i = 0
        while i < len(num) and num[i].isnumeric():
            i += 1
        
        num = num[:i]


        try:
            section_obj = sections.get(begin=num)
        except:
            return ""
        begin = num

    new_status = Status(status=status)
    new_status_data = StatusData(status_data=fragment, user=User.objects.get(name=owner.username))

    new_status.save()
    new_status_data.save()

    setattr(section_obj, "status", new_status)
    setattr(section_obj, "status_data", new_status_data)

    section_obj.save()

    return begin 


def html_tree(owner):
    dirs_and_files = get_dirs_and_files(owner)

    tree = ""
    
    for dir in dirs_and_files:
        tree += """<button id="dir_name_""" + dir[0].name + """" class="white" onclick="deleteDirectory('""" + dir[0].name + """')">"""

        for _ in dir[1]:
            tree += '&emsp;'
        tree += ' ' + dir[0].name + '/'

        tree += '</button>'

        for file in dir[2]:
            tree += """<button id="file_name_""" + file.name + """" onclick="fileClick('""" + file.name + """')">"""

            for _ in dir[1]:
                tree += '&emsp;'

            tree += '&emsp;| ' + file.name
            tree += '</button>'

    return tree