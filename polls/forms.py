from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm


class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=100)
    choice_text_1 = forms.CharField(max_length=100)
    choice_text_2 = forms.CharField(max_length=100)
    choice_text_3 = forms.CharField(max_length=100)


# class ChangePasswordForm(PasswordChangeForm):

class EmailChangeForm(forms.Form):
    error_messages = {
        'email_mismatch': ("The two e-mail address fields do not match."),
        'email_inuse': ("This e-mail address cannot be used. Please select a different e-mail address."),
        'password_incorrect': ("Incorrect password."),
    }

    current_password = forms.CharField(
        label=("Current Password"),
        widget=forms.PasswordInput,
        required=True
    )

    new_email1 = forms.EmailField(
        label=("New E-mail Address"),
        max_length=254,
        required=True
    )

    new_email2 = forms.EmailField(
        label=("Confirm New E-mail Address"),
        max_length=254,
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        """
        Validates that the password field is correct.
        """
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect',)
        return current_password

    def clean_new_email1(self):
        """
        Prevents an e-mail address that is already registered from being registered by a different user.
        """
        email1 = self.cleaned_data.get('new_email1')
        if User.objects.filter(email=email1).count() > 0:
            raise forms.ValidationError(self.error_messages['email_inuse'], code='email_inuse',)
        return email1

    def clean_new_email2(self):
        """
        Validates that the confirm e-mail address's match.
        """
        email1 = self.cleaned_data.get('new_email1')
        email2 = self.cleaned_data.get('new_email2')
        if email1 and email2:
            if email1 != email2:
                raise forms.ValidationError(self.error_messages['email_mismatch'], code='email_mismatch',)
        return email2

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email1']
        if commit:
            self.user.save()
        return self.user
