from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course
from .forms import ModuleFormSet


# Create your views here.


class OwnerMixin(object):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'manage/course/form.html'


"""Lists the courses created by the user. It inherits 
from OwnerCourseMixin and ListView. It defines a specific template_name
attribute for a template to list courses"""


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'manage/course/list.html'
    permission_required = 'courses.view_course'


""" Uses a model form to create a new Course object. 
It uses the fields defined in OwnerCourseMixin to build a model 
form and also subclasses CreateView. It uses the template defined 
in OwnerCourseEditMixin"""


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


"""Allows the editing of an existing Course object. 
It uses the fields defined in OwnerCourseMixin to build a model 
form and also subclasses UpdateView. It uses the template defined 
in OwnerCourseEditMixin."""


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


""" Inherits from OwnerCourseMixin and the generic 
DeleteView. It defines a specific template_name attribute for a template 
to confirm the course deletion.
"""


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'manage/module/formset.html'
    course = None

    """You define this method to avoid repeating the code to build 
    the formset. You create a ModuleFormSet object for the given Course object 
    with optional data"""
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)


    """: This method is provided by the View class. It takes an HTTP 
request and its parameters and attempts to delegate to a lowercase method 
that matches the HTTP method used. A GET request is delegated to the get()
method and a POST request to post(), respectively. In this method, you use 
the get_object_or_404() shortcut function to get the Course object for the 
given id parameter that belongs to the current user. You include this code in 
the dispatch() method because you need to retrieve the course for both GET
and POST requests. You save it into the course attribute of the view to make 
it accessible to other methods."""
    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.User)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})
