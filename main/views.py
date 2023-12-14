from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView

from main.forms import ClientForm, MailingForm, MsgForm
from main.models import Client, Mailing, Msg, Logfile


class HomeView(TemplateView):
    template_name = 'main/home.html'


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


class ClientDeleteView(DeleteView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')


class ClientListView(ListView):
    model = Client
    template_name = 'main/client_list.html'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')

    def form_valid(self, form):
        if form.is_valid:
            new_mailing= form.save()
            new_mailing.user = self.request.user
            new_mailing.save()

        return super().form_valid(form)


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')


class MailingDeleteView(DeleteView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('main:mailing_list')


class MailingListView(ListView):
    model = Mailing
    template_name = 'main/mailing_list.html'


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


class MessageUpdateView(UpdateView):
    model = Msg
    form_class = MsgForm
    success_url = reverse_lazy('main:msg_list')


class MessageDeleteView(DeleteView):
    model = Msg
    form_class = MsgForm
    success_url = reverse_lazy('main:msg_list')


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
