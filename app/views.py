from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import User, Directory, File, SectionCategory, Status, StatusData, FileSection
from .forms import FileForm, DirectoryForm
from .functions import dir_array, dir_array_levels, file_array, merge_dirs_files, get_dirs_and_files, delete_dir

# Create your views here.

def index_view(request):
    context = {
        'dirs_and_files': get_dirs_and_files(),
        'file_content': 'Choose a file!'
    }
    return render(request, 'app/index.html', context)


def add_file_view(request):
    form = FileForm()
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/')
    # else:

    context = {
        'form': form
    }
    return render(request, "app/add_file.html", context)


def add_directory_view(request):
    form = DirectoryForm()
    if request.method == "POST":
        form = DirectoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/app/')
    # else:

    context = {
        'form': form
    }
    return render(request, "app/add_directory.html", context)


def show_file_view(request, name):
    file_obj = get_object_or_404(File, name=name)

    f = open(file_obj.file.path, 'r')
    file_content = f.read()
    f.close()

    context = {
        'dirs_and_files': get_dirs_and_files(),
        'file_content': file_content,
    }
    return render(request, "app/index.html", context)


def delete_view(request):
    context = {
        'files': File.objects.filter(availability=True),
        'directories': Directory.objects.filter(availability=True),
    }
    return render(request, "app/delete.html", context)
    

def delete_file(request):
    try:
        selected_file = File.objects.get(name=request.POST['file'])
    except (KeyError, File.DoesNotExist):
        print("Didn't select a choice")
        return HttpResponseRedirect('/app/')
    else:
        selected_file.availability = False
        selected_file.save()
        return HttpResponseRedirect('/app/')


def delete_directory(request):
    try:
        selected_directory = Directory.objects.get(name=request.POST['directory'])
    except (KeyError, Directory.DoesNotExist):
        print("Didn't select a choice")
        return HttpResponseRedirect('/app/')
    else:
        delete_dir(selected_directory)
        return HttpResponseRedirect('/app/')




# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))