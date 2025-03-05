from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from account.forms import CustomPasswordChangeForm


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "account/auth/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('account:password-change-done')


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "account/auth/password_change_done.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = "account/auth/password_reset.html"
    email_template_name = "account/auth/password_reset_email.html"
    success_url = reverse_lazy('account:password-reset-done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "account/auth/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "account/auth/password_reset_confirm.html"
    success_url = reverse_lazy('account:password-reset-complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "account/auth/password_reset_complete.html"