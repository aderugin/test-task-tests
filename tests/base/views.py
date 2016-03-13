# -*- coding: utf-8 -*-
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from .models import Test, UserTesting
from .forms import QuestionForm


class TestListView(ListView):
    model = Test
    template_name = 'test_list.html'


class UserTestingView(TemplateView):
    template_name = 'test_detail.html'

    @method_decorator(login_required(login_url=reverse_lazy('login')))
    def dispatch(self, request, *args, **kwargs):
        self.test = get_object_or_404(Test, pk=kwargs['pk'])
        self.user_testing = self.get_user_testing()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.test
        context['user_testing'] = self.user_testing
        context['result'] = self.user_testing.get_result()
        if not self.user_testing.state_done:
            context['form'] = kwargs.get('form', self.get_form())
        return context

    def get_user_testing(self):
        return UserTesting.get(test=self.test, user=self.request.user)

    def post(self, request, *args, **kwargs):
        form = self.get_form(request.POST)
        if form.is_valid():
            self.user_testing.add_choice(
                form.question,
                form.cleaned_data['question']
            )
            if not self.user_testing.get_next_question():
                self.user_testing.finish()
            return HttpResponseRedirect(reverse('tests:test-detail', args=(self.test.id,)))
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_form(self, data=None):
        return QuestionForm(
            self.get_user_testing().get_next_question().id,
            data
        )


class AuthenticationView(TemplateView):
    template_name = 'authentication.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(request.GET.get('next', '/'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(request.GET.get('next', '/'))
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', AuthenticationForm())
        return context


class RegistrationView(TemplateView):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(request.GET.get('next', '/'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.GET.get('next', '/'))
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', UserCreationForm())
        return context


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout(request)
        return HttpResponseRedirect(request.GET.get('next', '/'))
