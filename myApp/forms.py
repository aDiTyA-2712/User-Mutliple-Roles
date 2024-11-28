# forms.py
from django import forms
from .models import User, Role

class UserRegistrationForm(forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Roles"
    )

    class Meta:
        model = User
        fields = [
            'username', 'firstname', 'middlename', 'lastname', 
            'password', 'email', 'description', 'roles'
        ]

        widgets = {
            'password': forms.PasswordInput(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
            self.save_m2m()  # Save the many-to-many relationships
        return user
