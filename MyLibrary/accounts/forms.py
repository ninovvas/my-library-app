import form as form
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django import forms
from django.contrib.auth.models import Permission, Group
from django.forms import DateInput

from MyLibrary.accounts.models import Profile
from MyLibrary.common.helper import BootstrapFormMixin

UserModel = get_user_model()

PROFILE_FORM_FIELDS = ['email', 'password1', 'password2', 'first_name', 'last_name']


class CreateProfileForm(BootstrapFormMixin, UserCreationForm):

    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )
    # picture = forms.URLField(
    #     label='URL Picture'
    # )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'class': 'datepicker'})
    )
    #date = forms.DateField(widget=forms.DateInput(format='%m-%Y-%d'))
    #description = forms.CharField(
    #    widget=forms.Textarea,
    #)
    #email = forms.EmailField()

    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in PROFILE_FORM_FIELDS:
            self.fields[field_name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)
        group = Group.objects.get(name='app_default')
        group.user_set.add(user)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            #picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            #description=self.cleaned_data['description'],
            gender=self.cleaned_data['gender'],
            user=user,
        )

        if commit:
            profile.save()

        return user

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name','date_of_birth')
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }



class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture', 'description', 'date_of_birth',)
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
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter description',
                    'rows': 3,
                },
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'placeholder': 'Date of Birth',
                }
            )
        }