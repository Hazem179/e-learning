from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Course


# Create your views here.


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


"""Lists the courses created by the user. It inherits 
from OwnerCourseMixin and ListView. It defines a specific template_name
attribute for a template to list courses"""


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'


""" Uses a model form to create a new Course object. 
It uses the fields defined in OwnerCourseMixin to build a model 
form and also subclasses CreateView. It uses the template defined 
in OwnerCourseEditMixin"""


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass


"""Allows the editing of an existing Course object. 
It uses the fields defined in OwnerCourseMixin to build a model 
form and also subclasses UpdateView. It uses the template defined 
in OwnerCourseEditMixin."""


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass


""" Inherits from OwnerCourseMixin and the generic 
DeleteView. It defines a specific template_name attribute for a template 
to confirm the course deletion.
"""


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
