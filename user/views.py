from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView  # Импорт LoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home")

    # Переопределяем метод form_valid для отправки письма после регистрации
    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     self.send_welcome_email(user.email)
    #     return super().form_valid(form)


    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True  # Активируем сразу для тестирования
        user.save()
        login(self.request, user)
        try:
            self.send_welcome_email(user.email)
        except Exception as e:
            print(f"Ошибка отправки email: {e}")  # Логируем ошибку, но не прерываем регистрацию
        return super().form_valid(form)


    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        recipient_list = [user_email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Перенаправлять уже авторизованных пользователей
    extra_context = {'title': 'Авторизация'}

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetTestView(TemplateView):
    template_name = 'users/password_reset_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        user = self.request.user
        context['uid'] = urlsafe_base64_encode(force_bytes(user.pk))
        context['token'] = default_token_generator.make_token(user)
        return context