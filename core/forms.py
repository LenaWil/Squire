from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
    PasswordChangeForm as DjangoPasswordChangeForm, PasswordResetForm as DjangoPasswordResetForm,
    SetPasswordForm as DjangoPasswordResetConfirmForm)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import ExtendedUser as User
from core.models import MarkdownImage
from core.widgets import  ImageUploadMartorWidget
from utils.forms import UpdatingUserFormMixin, UserFormMixin

##################################################################################
# Defines general-purpose forms.
# @since 15 AUG 2019
##################################################################################


# LoginForm that changes the default AuthenticationForm
# It provides a different error message when passing invalid login credentials,
# and allows Inactive users to login
class LoginForm(AuthenticationForm):
    def clean(self):
        # Obtain username and password
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Check if both are provided
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                # Invalid credentials provided
                self.add_error(None, ValidationError(
                    _("The username and/or password you specified are not correct."),
                    code='ERROR_INVALID_LOGIN',
                    params={'username': self.username_field.verbose_name},
                ))
                return
            # else:
                # Valid credentials provided
        return self.cleaned_data


# RegisterForm that expands on the default UserCreationForm
# It requires a (unique) email address, and includes an optional nickname field
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    nickname = forms.CharField(label = "Nickname", required=False, help_text='A nickname (if provided) is shown instead of your username.')

    class Meta:
        model = User
        fields = ("username", "nickname", "email")

    def clean_email(self):
        # Ensure that another user with the same email does not exist
        cleaned_email = self.cleaned_data.get('email')
        if User.objects.filter(email=cleaned_email).exists():
            self.add_error('email', ValidationError(
                _("A user with that email address already exists."),
                code='ERROR_EMAIL_EXISTS',
            ))
        return cleaned_email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        # First name field is used as a nickname field
        user.first_name = self.cleaned_data["nickname"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user

# Adds the relevant bootstrap classes to the password change form
class PasswordChangeForm(DjangoPasswordChangeForm):
    pass

# Adds the relevant bootstrap classes to the password reset form
class PasswordResetForm(DjangoPasswordResetForm):
    pass

class PasswordResetConfirmForm(DjangoPasswordResetConfirmForm):
    pass

class MarkdownForm(UserFormMixin, ModelForm):
    """
        Changes fields listed in markdown_field_names to use Martor's Markdown widget
        instead of their normal widget. Ideally, those fields should be TextFields, but this
        is not enforced.

        Also ensures that any images uploaded through Martor's widget are properly linked
        to the object that is being edited (if any). If an image is uploaded for an object
        that does not yet exist, then these images are temporarily unlinked (and do not reference)
        any object. Upon saving, if such "orphan" images exist (for the current model, and uploaded by
        the current user), they are linked to the newly created instance.
    """
    markdown_field_names = []
    placeholder_detail_title = "Field %s"

    is_new_instance = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_new_instance = self.instance.id is None

        for field_name in self.markdown_field_names:
            # Basic validation
            if field_name not in self.fields:
                # The passed field must actually exists
                raise ImproperlyConfigured(
                    "Form '%s' does not have a field '%s', "
                    "but this was passed in markdown_field_names." % (
                        self.__class__.__name__,
                        field_name,
                    )
                )
            elif not isinstance(self.fields[field_name], forms.CharField):
                # The passed field must be a Charfield, as there is no point to Markdown otherwise
                raise ImproperlyConfigured(
                    "Markdown cannot be rendered for Field %s of Form %s as it is not a Charfield, "
                    "but this field was passed in markdown_field_names." % (
                        field_name,
                        self.__class__.__name__,
                    )
                )

            # Add the field's label to the placeholder title
            label = self.fields[field_name].label
            placeholder_title = self.placeholder_detail_title % label.capitalize()

            # Replace the field's widget by Martor's markdown widget
            self.fields[field_name].widget = ImageUploadMartorWidget(
                ContentType.objects.get_for_model(self.instance),
                self.instance.id, placeholder_detail_title=placeholder_title
            )

    def _save_m2m(self):
        super()._save_m2m()

        # Handle "orphan" images that were uploaded when the instance was not yet saved
        #   to the database.
        if self.is_new_instance and self.user is not None:
            # Assign MarkdownImages for this contenttype, and uploaded by the requesting user
            content_type = ContentType.objects.get_for_model(self.instance)
            MarkdownImage.objects.filter(content_type=content_type, object_id__isnull=True).update(
                object_id=self.instance.id,
                uploader=self.user
            )

class MarkdownImageAdminForm(UpdatingUserFormMixin, ModelForm):
    class Meta:
        model = MarkdownImage
        fields = "__all__"

    updating_user_field_name = "uploader"
