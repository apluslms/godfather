from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from manage_course.models import CourseRepository
from manage_course.forms import RepoForm
from django.contrib import messages
from django.forms.models import model_to_dict
from django.contrib.auth import views as auth
import random, string
# Create your views here.

def overview(request):
    name = request.user.username
    courses = CourseRepository.objects.filter(owner=name)
    args = {'name': name, 'courses': courses}
    return render(request, 'manage_course/overview.jinja2', args)



def delete_course(request, key):
    course_to_delete = get_object_or_404(CourseRepository, key=key)
    if request.user.username == course_to_delete.owner:
        course_to_delete.delete()
        messages.success(request, 'The course was successfully deleted!')
        return redirect(overview)
    else:
        messages.error(request, 'The course was not deleted, something went wrong!')

def edit_course(request, key):
    course_to_edit = get_object_or_404(CourseRepository, key=key)
    form = RepoForm(initial=model_to_dict(course_to_edit))
    args = {'form': form}

    if request.method == 'POST':
        form = RepoForm(request.POST, instance=course_to_edit)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            messages.success(request, 'The course was successfully updated!')
            return redirect(overview)
        else:
             messages.error(request, 'The course was not updated, something went wrong!')
             return render(request, 'manage_course/edit_course.jinja2', args)
    else:
            # If the request was not a POST, display the form to enter details.
        return render(request, 'manage_course/edit_course.jinja2', args)
    return render(request, 'manage_course/edit_course.jinja2', args)




def create_course(request):
    #Generate a random key for repo url
    form = RepoForm(initial={'key': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7)), 'owner':request.user.username})
    args = {'form': form}

    if request.method == 'POST':
        form = RepoForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            messages.success(request, 'The course was successfully added!')
            # we should redirect after data modifying
            return redirect(overview)
        else:
             messages.error(request, 'The course was not added, something went wrong!')
             return render(request, 'manage_course/create_course.jinja2', args)
    else:
            # If the request was not a POST, display the form to enter details.
        return render(request, 'manage_course/create_course.jinja2', args)
