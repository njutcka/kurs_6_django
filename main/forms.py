from django import forms
from django.forms import ModelForm
from django.urls import reverse_lazy

from main.models import Client, Mailing, Msg


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'comment',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Msg.objects.filter(user=user)

    class Meta:
        model = Mailing
        exclude = ('user',)


class MailingModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ('title_mail', 'is_activated',)


class MsgForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Msg
        fields = ('msg_title', 'msg_body',)
