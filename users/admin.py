from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _

from users.models import User, Recruiter, Student, Major, Degree


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ['groups','user_permissions','username','email', 'is_admin','first_name','last_name','thumbnail_profile_pic','profile_pic']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        fields = ['groups','user_permissions','username','email', 'is_admin','first_name','last_name', 'thumbnail_profile_pic','profile_pic']
        
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','email', 'is_admin','first_name','last_name','thumbnail_profile_pic','profile_pic','linkedin_uid','time_created','last_login','is_verified','verification_token')
    list_filter = ('is_admin',)
    fieldsets = [
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'first_name','last_name','thumbnail_profile_pic','profile_pic')}),
        ('Permissions', {'fields': ('is_admin','groups','user_permissions')}),
    ]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2','first_name','last_name','thumbnail_profile_pic','profile_pic')}
        ),
    )
    search_fields = ('username','email',)
    ordering = ('username','email',)
    filter_horizontal = ()


class RecruiterAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2','first_name','last_name','thumbnail_profile_pic','profile_pic','company'),
        }),
    )
    list_display = UserAdmin.list_display + ('company',)

class StudentAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2','first_name','last_name','thumbnail_profile_pic','profile_pic','verified_email','graduation_year'),
        })
    )
    list_display = UserAdmin.list_display + ('verified_email', 'graduation_year')

class MajorAdmin(admin.ModelAdmin):
    list_display = ('major',)

class DegreeAdmin(admin.ModelAdmin):
    list_display = ('degree',)

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Recruiter, RecruiterAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Major, MajorAdmin)
admin.site.register(Degree, DegreeAdmin)
