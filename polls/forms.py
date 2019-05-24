from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class QuestionForm(forms.Form):
    question_text = forms.CharField(max_length=100)
    choice_text_1 = forms.CharField(max_length=100)
    choice_text_2 = forms.CharField(max_length=100)
    choice_text_3 = forms.CharField(max_length=100)


class ContactForm(forms.Form):
    from_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'style': 'border-color: orange;',
                   'placeholder': 'Enter email here'},
            ),
        help_text="We check this out, so type a real email!"
        )
    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'style': 'border-color: blue;',
                   'placeholder': 'Enter subject here'}
                ),
        help_text="Choose a real subject"
        )
    message = forms.CharField(
            widget=forms.Textarea(
                  attrs={'style': 'border-color: green',
                         'placeholder': 'Enter your message here'}
                   ),
            required=True,
            help_text="Write what you want here"
            )


class NamesForm(forms.Form):
    password_field = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(attrs={'style': 'border-color: green;',
                                          'placeholder': 'Enter password'}),
        required=True,
        help_text="I hope you know your password"
        )
    first_name = forms.CharField(max_length=30, widget=forms.Textarea(
                                 attrs={'style': 'border-color: yellow;',
                                        'placeholder': 'Enter first_name'}),
                                 help_text="First_name type here"
                                 )
    last_name = forms.CharField(max_length=150, widget=forms.Textarea(
                                attrs={'style': 'border-color: blue;',
                                       'placeholder': "Enter second_name"}),
                                help_text="Second_name type here")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(NamesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.add_input(Submit('submit', 'Save person'))

    def clean_current_password(self):
        """
        Validates that the password field is correct.
        """
        password_field = self.cleaned_data["password_field"]
        if not self.user.check_password(password_field):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect',)
        return password_field

    def save(self, commit=True):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        if commit:
            self.user.save()
        return self.user

# class ChangePasswordForm(PasswordChangeForm):


class EmailChangeForm(forms.Form):
    error_messages = {
        'email_mismatch': ("The two e-mail address fields do not match."),
        'email_inuse': ("This e-mail address cannot be used. Please select a different e-mail address."),
        'password_incorrect': ("Incorrect password."),
    }

    current_password = forms.CharField(
        label=("Current Password"),
        widget=forms.PasswordInput(
            attrs={
                'style': 'border-color:blue;',
                'placeholder': 'Write your pass here'
            }
        ),
        required=True,
        help_text="I hope you know your password"
    )

    new_email1 = forms.EmailField(
        label=("New E-mail Address"),
        widget=forms.EmailInput(attrs={'style': 'border-color: green;',
                                       'placeholder': 'Enter email'}),
        max_length=254,
        required=True,
        help_text='Type here new email'
    )

    new_email2 = forms.EmailField(
        label=("Confirm New E-mail Address"),
        widget=forms.EmailInput(attrs={'style': 'border-color: orange;',
                                       'placeholder': 'Enter email again'}),
        max_length=254,
        required=True,
        help_text='Confirm by typing email again'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

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
