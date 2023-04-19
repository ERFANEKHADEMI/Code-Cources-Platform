from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required

# models
from ..models import Tag, Course, CourseTask, CourseTitle

from ..forms import CourseForm

# services
from base.services import get_all_courses
from article.services import get_all_tags

# utils
from article.utils import checking_slug, slug_generator

def show_all_courses_view(request):
    # get all courses
    courses = Course.objects.all()
    
    context = {
        'courses': courses,
    }
    return render(request, 'course/showAllCourses.html', context)

def course(request, slug):
    # get course and titles
    course = Course.objects.get(slug=slug)
    
    lessons_count = 0
    videos_count = 0
    exercises_count = 0
    projects_count = 0
    
    for title in course.course_titles.all():
        for task in title.tasks.all():
            lessons_count += 1
            if task.taskType == 'video':
                videos_count += 1
            if task.taskType == 'code':
                exercises_count += 1
                
    context = {
        'course': course, 
         'videos_count': videos_count,
        'lessons_count': lessons_count,
        'exercises_count': exercises_count,
        'projects_count': projects_count
    }
    return render(request, 'course/CourseInfo.html', context)
 
@login_required(login_url='base:login')
def create_course_view(request):
    if request.user.is_superuser:
        form = CourseForm()
       
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
           
            if form.is_valid():
                slug = checking_slug(slug_generator(form.cleaned_data.get('title')))
                
                course = form.save(commit=False)
                course.user = request.user
                course.slug = slug
            
                form.save()
                return redirect('/profile/'+str(request.user.username)+'/courses')
            
        return render(request, 'course/AddNewCourse.html', { 'form': form})
    else:
        return redirect('base:registration')

@login_required(login_url='base:login')
def task_view(request, slug, pk):
    # get courses and tasks
    course = Course.objects.get(slug=slug)
    task =  CourseTask.objects.get(id=pk)
    titles = CourseTitle.objects.filter(course=course.id)
    # comments = CourseComment.objects.filter(course=course, courseTask=task)
    
    prev_page = ''
    next_page = ''
    
    # number = tasks.index(task)
    
    # try: 
    #     if (tasks[number+1]):
    #         next_page = tasks[number+1]
    # except:
    #     print('Error')
    
    # try: 
    #     if (tasks[number-1] and  number!=0):
    #         prev_page = tasks[number-1]
    # except:
    #     print('Error')
    
    if request.user.is_authenticated != True:
        return redirect('base:login')
    
    if request.method == 'POST':
        if (request.user.is_authenticated):
            # get data from form
            comment = request.POST.get('comment')
            
            # create a new Course
            form = CourseComment.objects.create(
                commentType = 'comment',
                course = course,
                user = request.user,
                # message = comment,
                # courseTask = task,
            )
            
            form.save()
            return redirect('courses:task', course.slug, task.id)
        else:
            return redirect('base:login')
    
    context = {
        'course': course,
        'task': task,
        
        'priv_page': prev_page,
        'next_page': next_page,
        
    }
    return render(request, 'course/Task.html', context)
    
@login_required(login_url='base:login')
def delete_course(request, slug):
   if request.user.is_superuser:
     # get article
        course = Course.objects.get(slug=slug)
        
        # check article and user
        if request.method == 'POST':
            if course.user.username == request.user.username:
                #delete article
                course.delete()
                return redirect('course:show_all_courses')
            else:
                messages.error(request, 'You are not allowed to delete this article')
        
        context = {
           'course': course
        }
        return render(request, 'course/DeleteCourse.html', context)
   else:
        return redirect('article:registration')
