from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# from django.template.defaultfilters import linebreaks
# from django.template.defaultfilters import linebreaksbr
# from django.utils.safestring import mark_safe


text_for_pass = (
    "<ul><li>Your password can't be too similar to your other personal information.</li>"
    "<li>Your password must contain at least 8 characters.</li>"
    "<li>Your password can't be a commonly used password.</li>"
    "<li>Your password can't be entirely numeric.</li></ul>"
    )


class QuestionForm(forms.Form):

    question_text = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'style': 'border-color: red;',
                   'placeholder': 'Enter your question here'},
            ),
        help_text="New question should be interesting!"
        )
    choice_text_1 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'style': 'border-color: green;',
                   'placeholder': 'Enter first choice here'},
            ),
        help_text="Type first choice!"
        )
    choice_text_2 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'style': 'border-color: orange;',
                   'placeholder': 'Enter second choice here'},
            ),
        help_text="Type second choice!"
        )
    choice_text_3 = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'style': 'border-color: blue;',
                   'placeholder': 'Enter third here'},
            ),
        help_text="Type third choice!"
        )


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
        required=True,
        widget=forms.Textarea(
              attrs={'style': 'border-color: green',
                     'placeholder': 'Enter your message here'}
               ),
        help_text="Write what you want here"
        )


class NamesForm(forms.Form):
    password_field = forms.CharField(
        required=True,
        label='Current password',
        widget=forms.PasswordInput(attrs={'style': 'border-color: green;',
                                          'placeholder': 'Enter password'}),
        help_text="I hope you know your password"
        )
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
                                 attrs={'style': 'border-color: yellow;',
                                        'placeholder': 'Enter first_name'}),
                                 help_text="First_name type here"
                                 )
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(
                                attrs={'style': 'border-color: blue;',
                                       'placeholder': "Enter second_name"}),
                                help_text="Second_name type here")

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(NamesForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))

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
        required=True,
        label=("Current Password"),
        widget=forms.PasswordInput(
            attrs={
                'style': 'border-color:blue;',
                'placeholder': 'Write your pass here'
            }
        ),

        help_text="I hope you know your password"
    )

    new_email1 = forms.EmailField(
        required=True,
        label=("New E-mail Address"),
        widget=forms.EmailInput(attrs={'style': 'border-color: green;',
                                       'placeholder': 'Enter email'}),
        max_length=254,
        help_text='Type here new email'
    )

    new_email2 = forms.EmailField(
        required=True,
        label=("Confirm New E-mail Address"),
        widget=forms.EmailInput(attrs={'style': 'border-color: orange;',
                                       'placeholder': 'Enter email again'}),
        max_length=254,
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


class PasswordChangeForm2(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: orange;',
                'placeholder': 'type here old password',
                'id': 'hi1',
            }),
        help_text="Check if it is really you are",
        )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: green;',
                'placeholder': 'type new password',
                'id': 'Imagine a new password',
            }),
        help_text=text_for_pass,
        )

    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: blue;',
                'placeholder': 'type new password again',
                'id': 'hi3',
            }),
        help_text="Check new password",
        )


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: blue;',
                'placeholder': 'type username',
            }),
            help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
            )
    email = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: green;',
                'placeholder': 'type email',
            }),
            )
    password1 = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: yellow;',
                'placeholder': 'type password here',
            }),
        help_text=text_for_pass,
            )
    password2 = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: red;',
                'placeholder': 'type password again',
            }),
            )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class PasswordChangeForm3(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: orange;',
                'placeholder': 'type here old password',
                'id': 'hi1',
            }),
        help_text="Check if it is really you are",
        )
    new_password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: green;',
                'placeholder': 'type new password',
                'id': 'Imagine a new password',
            }),
        help_text=text_for_pass,
        )

    new_password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: blue;',
                'placeholder': 'type new password again',
                'id': 'hi3',
            }),
        help_text="Check new password",
        )


class LoginForm(forms.Form):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    username = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: blue;',
                'placeholder': 'type username',
            }),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
            )
    password = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'style': 'border-color: red;',
                'placeholder': 'type password again',
            }),
        help_text="Type a strong password, which you will forget after few sec"
            )
