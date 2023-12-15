import random

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView, ListView

from users.forms import UserRegisterForm, UserProfileForm, UserModeratorForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_email')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Подтверждение почты',
                message=f'Код {new_user.ver_code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


class VerificationTemplateView(TemplateView):
    template_name = 'users/msg_email.html'

    def post(self, request):
        ver_code = request.POST.get('ver_code')
        user_code = User.objects.filter(ver_code=ver_code).first()

        if user_code is not None and user_code.ver_code == ver_code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verify_email_error')


class ErrorVerificationTemplateView(TemplateView):
    template_name = 'users/verify_email.html'
    success_url = reverse_lazy('users:msg_email')


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:home'))


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


class UsersModView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserModeratorForm
    success_url = reverse_lazy('users:user_list')
    permission_required = 'users.set_is_activated'
