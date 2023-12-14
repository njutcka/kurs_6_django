from django import forms
from django.forms import ModelForm
from django.urls import reverse_lazy

from main.models import Client, Mailing, Msg


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'comment',)


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        exclude = ('user',)


class MsgForm(ModelForm):
    class Meta:
        model = Msg
        fields = ('msg_title', 'msg_body',)
