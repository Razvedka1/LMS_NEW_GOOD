from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.db.models import Q

from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .models import Course, Lesson, Tracking, Review
from .forms import CourseForm, ReviewForm, LessonForm, OrderByAndSearchForm
from django.core.exceptions import NON_FIELD_ERRORS


class MainView(ListView, FormView):
    queryset = Course.objects.all()
    context_object_name = 'courses'
    #paginate_by = 2  # Указывает число в виде инт  сколько выводится в шаблон за 1 раз
    form_class = OrderByAndSearchForm

    def get_queryset(self):
        queryset = MainView.queryset
        if {'search', 'price_order'} != self.request.GET.keys():
            return queryset
        else:
            search_query = self.request.GET.get('search')
            price_order_by = self.request.GET.get('price_order',)
            filter = Q(title__icontains=search_query) | Q(description__icontains=search_query)
            queryset = queryset.filter(filter).order_by(price_order_by)
        return queryset
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context
    def get_initial(self):
        initial = super(MainView, self).get_initial()
        initial['search'] = self.request.GET.get('search', '')
        initial['price_order'] = self.request.GET.get('price_order', 'title')
        return initial


class CourseDetailView(ListView):
    model = Lesson
    template_name = 'detail.html'
    context_object_name = 'lessons'
    pk_url_kwarg = 'course_id'


    def get_queryset(self):
        return Lesson.objects.select_related('course').filter(course=self.kwargs.get('course_id'))

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['reviews'] = Review.objects.select_related('user').filter(course=self.kwargs.get('course_id'))
        return context


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'create.html'

    permission_required = ('learning.add_course',)

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})


    def form_valid(self, form):
        with transaction.atomic():
            course = form.save(commit=False)
            course.author = self.request.user
            course.save()
            return super(CourseCreateView, self).form_valid(form)


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'create.html'
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.change_course',)

    def get_queryset(self):
        return Course.objects.filter(id=self.kwargs.get('course_id'))

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.object.id})

class LessonCreateView(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Lesson
    form_class = LessonForm
    template_name = 'create_lesson.html'
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.add_lesson',)

    def get_success_url(self):
        return reverse('detail', kwargs={'course_id': self.kwargs.get('course_id')})

    def get_form(self, form_class=None):
        form = super(LessonCreateView, self).get_form()
        form.fields['course'].queryset = Course.objects.filter(authors=self.request.user)
        return form


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'delete.html'
    pk_url_kwarg = 'course_id'

    permission_required = ('learning.delete_course',)

    # 1
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
# 2



@transaction.atomic
@login_required
@permission_required('learning.add_tracking', raise_exception=True)
def enroll(request, course_id):
    # if request.user.is_anonymous:
    # return redirect('login')
    #  else:
    is_existed = Tracking.objects.filter(user=request.user, lesson__course=course_id).exists()
    if is_existed:
        return HttpResponse(f'Здесь мы сможем записаться на выбранный курс')
    else:
        lessons = Lesson.objects.filter(course=course_id)
        records = [Tracking(lesson=lesson, user=request.user, passed=False) for lesson in lessons]
        Tracking.objects.bulk_create(records)
        return HttpResponse('Вы записаны на данный курс')


@login_required()
@permission_required('learning.add_review', raise_exception=False)
def review(request, course_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.errors:
            errors = form.errors[NON_FIELD_ERRORS]
            return render(request, 'review.html', {'form': form, 'errors': errors})
        if form.is_valid():
            data = form.cleaned_data
            Review.objects.create(content=data['content'],
                                  course=Course.objects.get(id=course_id),
                                  user=request.user)
        return redirect(reverse('detail', kwargs={'course_id': course_id}))
    else:
        form = ReviewForm()
        return render(request, 'review.html', {'form': form})
