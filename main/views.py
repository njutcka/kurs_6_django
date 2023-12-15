import random

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView

from blog.models import Blog
from main.forms import ClientForm, MailingForm, MsgForm, MailingModeratorForm
from main.models import Client, Mailing, Msg, Logfile


def get_cache_for_mailings():
    if settings.CACHE_ENABLED:
        key = 'mailings_count'
        mailings_count = cache.get(key)
        if mailings_count is None:
            mailings_count = Mailing.objects.all().count()
            cache.set(key, mailings_count)
    else:
        mailings_count = Mailing.objects.all().count()
    return mailings_count


def get_cache_clients():
    if settings.CACHE_ENABLED:
        key = 'client_count'
        client_count = cache.get(key)
        if client_count is None:
            client_count = len(Client.objects.all())
            cache.set(key, client_count)
    else:
        client_count = len(Client.objects.all())
    return client_count


def get_cache_for_active_mailings():
    if settings.CACHE_ENABLED:
        key = 'active_mailings_count'
        active_mailings_count = cache.get(key)
        if active_mailings_count is None:
            active_mailings_count = Mailing.objects.filter(is_activated=True).count()
            cache.set(key, active_mailings_count)
    else:
        active_mailings_count = Mailing.objects.filter(is_activated=True).count()
    return active_mailings_count


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailings_count'] = get_cache_for_mailings()
        context_data['active_mailings_count'] = get_cache_for_active_mailings()
        context_data['client_count'] = get_cache_clients()
        blog_list = list(Blog.objects.all())
        random.shuffle(blog_list)
        context_data['blog_list'] = blog_list[:3]
        return context_data


class MyMailing(LoginRequiredMixin, TemplateView):
    template_name = 'main/my_mailing.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')

    def form_valid(self, form):
        if form.is_valid:
            new_client = form.save()
            new_client.user = self.request.user
            new_client.save()

        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class ClientDeleteView(DeleteView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class ClientListView(ListView):
    model = Client
    template_name = 'main/client_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список рассылок'
        return context

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.has_perm('mailing.view_mailing'):
            return Client.objects.all()
        queryset = Client.objects.filter(user=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        if form.is_valid:
            new_mailing= form.save()
            new_mailing.user = self.request.user
            new_mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def test_func(self):
        return self.request.user == Mailing.objects.get(pk=self.kwargs['pk']).user


class MailingUpdateModView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingModeratorForm
    success_url = reverse_lazy('main:mailing_list')
    permission_required = 'main.set_is_activated'


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('main:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список рассылок'
        return context

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.has_perm('mailing.view_mailing'):
            return Mailing.objects.all()
        queryset = Mailing.objects.filter(user=self.request.user, is_activated=True)
        return queryset


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'main/mailing_detail.html'


class MessageCreateView(CreateView):
    model = Msg
    form_class = MsgForm
    success_url = reverse_lazy('main:msg_list')

    def form_valid(self, form):
        if form.is_valid:
            new_msg = form.save()
            new_msg.user = self.request.user
            new_msg.save()

        return super().form_valid(form)


class MessageListView(ListView):
    model = Msg
    template_name = 'main/msg_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список рассылок'
        return context

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.has_perm('mailing.view_mailing'):
            return Msg.objects.all()
        queryset = Msg.objects.filter(user=self.request.user)
        return queryset


class MessageUpdateView(UpdateView):
    model = Msg
    form_class = MsgForm
    success_url = reverse_lazy('main:msg_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class MessageDeleteView(DeleteView):
    model = Msg
    form_class = MsgForm
    success_url = reverse_lazy('main:msg_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class LogsListView(ListView):
    model = Logfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Отчет об отправленных рассылках'
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            return Logfile.objects.all()
        queryset = Logfile.objects.filter(mailing__user=self.request.user)
        return queryset
