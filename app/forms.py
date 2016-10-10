from django import forms
from django.core.files.images import get_image_dimensions
from django.contrib.auth.models import User

from app.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email)\
        .exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use.\
             Please supply a different email address.')

        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    """
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        try:
            w, h = get_image_dimensions(avatar)

            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            
            Handles case when we are updating the user profile
            and do not supply a new avatar
            
            pass

        return avatar


    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=True)
        #user.avatar = self.cleaned_data.get('avatar')

        if commit:
            user.save()

        return user
    """