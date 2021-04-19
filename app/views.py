from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import User, Directory, File, SectionCategory, Status, StatusData, FileSection
from .forms import FileForm

# Create your views here.

def index_view(request):
    files = File.objects.all()
    context = {
        'files': files,
        'file_content': ''
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


def show_file_view(request, name):
    file_obj = get_object_or_404(File, name=name)

    f = open(file_obj.file.path, 'r')
    file_content = f.read()
    f.close()

    context = {
        'file_content': file_content,
        'files': File.objects.all(),
    }
    return render(request, "app/index.html", context)


def delete_view(request):
    files = File.objects.all()
    context = {
        'files': files,
    }
    return render(request, "app/delete.html", context)
    

def delete_file(request):
    try:
        selected_file = File.objects.get(name=request.POST['file'])
        # selected_file = file_obj.choice_set.get(pk=request.POST['choice'])
    except (KeyError, File.DoesNotExist):
        # Redisplay the question voting form.
        # return render(request, 'polls/detail.html', {
        #     'question': question,
        #     'error_message': "You didn't select a choice.",
        # })
        print("didnt select a choice")
    else:
        #delete file
        return HttpResponseRedirect('/app/')


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

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