from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Directory, File, SectionCategory, Status, StatusData, FileSection
from .forms import FileForm, DirectoryForm, VCsForm, tab_options
from .functions import dir_array, dir_array_levels, file_array, merge_dirs_files, get_dirs_and_files, delete_dir, get_result, create_sections, get_command, basic_compile, adv_compile, parse_compilation, html_tree
import os
import subprocess

# Create your views here.

@login_required
def index_view(request):
    if request.session.get("file_content") == None:
        request.session["file_content"] = 'Choose a file!'

    if request.session.get("active_tab") == None:
        request.session["active_tab"] = "prover"

    if request.session.get("rte") == None:
        request.session["rte"] = False

    if request.session.get("prover") == None:
        request.session["prover"] = "None"

    context = {
        'dirs_and_files': get_dirs_and_files(request.user),
        'file_content': request.session.get("file_content"),
        'chosen_file': request.session.get("chosen_file"),
        'active_tab': request.session.get("active_tab"),
        'result': request.session.get("result"),
        'options': tab_options.get(request.session.get("active_tab")),
        'form': VCsForm,
        'vcs': request.session.get("vcs"),
        'rte': request.session.get("rte"),
        'prover': request.session.get("prover"),
        'compile_result': request.session.get("compile_result"),
    }
    return render(request, 'app/index.html', context)


@login_required
def add_file_view(request):
    form = FileForm()
    form.fields["directory"].queryset = Directory.objects.filter(availability=True, owner=request.user.username)

    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        form.fields["directory"].queryset = Directory.objects.filter(availability=True, owner=request.user.username)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = User.objects.get(name=request.user.username)
            f.save()
            create_sections(f)
            return HttpResponseRedirect('/app/')

    context = {
        'form': form
    }
    return render(request, "app/add_file.html", context)


@login_required
def add_directory_view(request):
    form = DirectoryForm()
    form.fields["parent_directory"].queryset = Directory.objects.filter(availability=True, owner=request.user.username)
    if request.method == "POST":
        form = DirectoryForm(request.POST)
        form.fields["parent_directory"].queryset = Directory.objects.filter(availability=True, owner=request.user.username)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = User.objects.get(name=request.user.username)
            f.save()
            return HttpResponseRedirect('/app/')

    context = {
        'form': form
    }
    return render(request, "app/add_directory.html", context)


@login_required
def show_tab(request, tab):
    request.session["active_tab"] = tab

    form = None

    if tab == "result":
        chosen_file = request.session.get("chosen_file")
        if chosen_file != None:
            file = get_object_or_404(File, name=chosen_file)
            if request.session.get("result") == None:
                request.session["result"] = get_result(file)

    elif tab == "vcs":
        form = VCsForm

    context = {
        'dirs_and_files': get_dirs_and_files(request.user),
        'file_content': request.session.get("file_content"),
        'chosen_file': request.session.get('chosen_file'),
        'active_tab': request.session.get("active_tab"),
        'result': request.session.get("result"),
        'options': tab_options.get(tab),
        'form': form,
        'vcs': request.session.get("vcs"),
        'rte': request.session.get("rte"),
        'prover': request.session.get("prover"),
        'compile_result': request.session.get("compile_result"),
    }
    return render(request, "app/index.html", context)


@login_required
def save_prover(request):
    if request.method == 'POST':
        request.session["prover"] = request.POST.get("prover")
    
    tab = "provers"

    return redirect('app:show_tab', tab)


@login_required
def save_vcs(request):
    if request.method == 'POST':
        request.session["vcs"] = request.POST.getlist('vcs')
        form = VCsForm(request.POST)

        if request.POST.get("rte") == "on":
            request.session["rte"] = True
        else:
            request.session["rte"] = False

    else:
        form = VCsForm
    
    tab = "vcs"

    return redirect('app:show_tab', tab)


@login_required
def auth_user(request):
    user = User.objects.filter(login=request.user.username)
    if not user:
        user = User(
            name=request.user.username,
            login=request.user.username,
            password=request.user.password)
        user.save()

    return HttpResponseRedirect('/app')


@login_required
def js_show_file(request):
    name = request.GET.get("name", None)
    previous = "true"

    if name != request.session.get("chosen_file"):
        previous = "false"
        request.session["chosen_file"] = name
        request.session["compile_result"] = None

        
        file_obj = get_object_or_404(File, name=name)

        with open(file_obj.file.path, 'r') as file:
            file_content = list(file)

        formatted_content = ""

        for idx, line in enumerate(file_content):
            file_content[idx] = (line, idx + 1)
            formatted_content += str(idx + 1) + "   " + line

        request.session["file_content"] = formatted_content

        if request.session.get("active_tab") == "result":
            request.session["result"] = get_result(file_obj)
        else:
            request.session["result"] = None

    data = {
        "previous": previous,
        "content": request.session.get("file_content"),
        "result": request.session.get("result")
    }

    return JsonResponse(data)


@login_required
def js_delete_file(request):
    name = request.GET.get("name", None)

    selected_file = get_object_or_404(File, name=name)
    selected_file.availability = False
    selected_file.save()

    data = {
        "tree": html_tree(request.user),
    }

    return JsonResponse(data)


@login_required
def js_delete_directory(request):
    name = request.GET.get("name", None)

    selected_directory = get_object_or_404(Directory, name=name)
    delete_dir(selected_directory)

    data = {
        "tree": html_tree(request.user),
    }

    return JsonResponse(data)


@login_required
def js_compile(request):
    file_name = request.session.get("chosen_file")
    rte = request.session.get("rte")
    prover = request.session.get("prover")
    vcs = request.session.get("vcs")
    adv = False

    if file_name == None:
        return JsonResponse({})

    command = get_command(file_name, rte, prover, vcs)

    if rte == False and prover == "None" and not vcs:
        compile_result = basic_compile(file_name)
    else:
        compile_result = adv_compile(file_name, command)
        adv = True

    parsed_result = parse_compilation(compile_result, file_name, adv, request.user)

    text = ""
    
    for idx, x in enumerate(parsed_result):
        if x[0] != '' and x[3] != '':
            text += '<div class="pointer frama_' + x[0] + '" onclick="toggleDisplay(' + "'id_sect_" + str(idx) + "'" + ')"><p>' + x[1]

            text += '- line ' + x[3]

            text += '</p></div>'

        text += '<div id="id_sect_' + str(idx) + '" class="frama_' + x[0] + '" style="display:none;"><p>' + x[2] + '</p></div>'
        
    request.session["compile_result"] = text

    data = {
        "compile_result": text,
    }

    return JsonResponse(data)