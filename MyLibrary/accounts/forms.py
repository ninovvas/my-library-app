from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms

from MyLibrary.accounts.models import Profile
from MyLibrary.common.helper import BootstrapFormMixin

UserModel = get_user_model()

PROFILE_FORM_FIELDS = ['email', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'description']

class CreateProfileForm(BootstrapFormMixin, UserCreationForm):


    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )
    picture = forms.URLField()
    date_of_birth = forms.DateField()
    description = forms.CharField(
        widget=forms.Textarea,
    )
    #email = forms.EmailField()

    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self._init_bootstrap_form_controls()

        for field_name in PROFILE_FORM_FIELDS:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            description=self.cleaned_data['description'],
            #email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user,
        )
        # profile = Profile(
        #     **self.cleaned_data,
        #     user=user,
        # )

        if commit:
            profile.save()

        return user

    class Meta:
        model = UserModel
        fields = PROFILE_FORM_FIELDS
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL',
                }
            ),
        }