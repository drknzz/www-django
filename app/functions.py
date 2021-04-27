from .models import User, Directory, File, SectionCategory, Status, StatusData, FileSection

#returns array of directories with child order
def dir_array(parent_dir):
    dirs = Directory.objects.filter(parent_directory=parent_dir, availability=True)
    array = []
    for dir in dirs:
        array.append(dir)
        array = array + dir_array(dir)
    return array

#adds to each directory in array its level
def dir_array_levels(dir_array):
    array = []
    for dir in dir_array:
        array.append([dir, range(dir.level)])
    return array

#returns array of arrays of files in order of directories from dir_array
def file_array(dir_array):
    array = []
    for dir in dir_array:
        files = File.objects.filter(directory=dir[0], availability=True)
        array.append(files)
    return array

#merges list of dirs with list of files
def merge_dirs_files(dirs, files):
    for idx, dir in enumerate(dirs):
        dir.append(files[idx])
    return dirs

#returns list of dirs with their files
def get_dirs_and_files():
    dirs = dir_array_levels(dir_array(None))
    files = file_array(dirs)
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
