from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Course, Lesson, Tracking
from django import forms


class MainView(ListView):
    queryset = Course.objects.all()
    context_object_name = 'courses'
    paginate_by = 2  # Указывает число в виде инт  сколько выводится в шаблон за 1 раз

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context


class CourseDetailView(DetailView):
    template_name = 'detail.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.filter(course=self.kwargs.get('course_id'))
        return context


class CourseCreateView(CreateView):
    model = Course
    form_class = Course
    template_name = 'create.html'

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})

    def form_valid(self, form):
        course = form.save(commit=False)
        course.author = self.request.user
        course.save()
        return super(CourseCreateView, self).form_valid(form)


class CourseUpdateView(UpdateView):
    model = Course
    form_class = Course
    template_name = 'create.html'
    pk_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'delete.html'
    pk_url_kwarg = 'course_id'

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('index')


# def index(request):
# courses = Course.objects.all()
# current_year = datetime.now().year
# return render(request, context={'courses': courses, 'current_year': current_year}, template_name='index.html')


# def create(request):
#    if request.method == 'POST':
#        data = request.POST
#        Course.objects.create(title=data['title'], author=request.user,
#  description=data['description'], start_date=data['start_date'],
#  duration=data['duration'], price=data['price'],
# count_lessons=data['count_lessons'])
#        return redirect('index')
#    else:
#       return render(request, 'create.html')


# def delete(request, course_id):
#    Course.objects.get(id=course_id).delete()
#    return redirect('index')


# def detail(request, course_id):
#    course = Course.objects.get(id=course_id)
#    lessons = Lesson.objects.filter(course=course_id)
#    context = {'course': course, 'lessons': lessons}
#    return render(request, 'detail.html', context)


def enroll(request, course_id):
    if request.user.is_anonymous:
        return redirect('login')
    else:
        is_existed = Tracking.objects.filter(user=request.user, lesson__course=course_id).exists()
        if is_existed:
            return HttpResponse(f'Здесь мы сможем записаться на выбранный курс')
        else:
            lessons = Lesson.objects.filter(course=course_id)
            records = [Tracking(lesson=lesson, user=request.user, passed=False) for lesson in lessons]
            Tracking.objects.bulk_create(records)
            return HttpResponse('Вы записаны на данный курс')
