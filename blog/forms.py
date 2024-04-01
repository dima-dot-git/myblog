from django import forms
from .models import Post, Subscribe, Comment, User, PostsPhoto, Profile_WER, Tag
from django.forms import inlineformset_factory, ClearableFileInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["published_data", "user"]


class AddTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['post']


class PostsPhotoForm(forms.ModelForm):
    class Meta:
        model = PostsPhoto
        exclude = ["post"]


PostsPhotoFormSet = inlineformset_factory(Post, PostsPhoto, form=PostsPhotoForm, extra=1)


class ProfileWERForm(forms.ModelForm):
    class Meta:
        model = Profile_WER
        exclude = ["user"]


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['date']


class RegUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class ChangeUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_user_data = self.instance
        for field_name in self.fields:
            self.fields[field_name].required = False

    def clean(self):
        cleaned_data = super().clean()
        updated_data = {}
        for field_name, field_value in cleaned_data.items():
            current_value = getattr(self.current_user_data, field_name)
            if field_value != current_value and field_value != "":
                updated_data[field_name] = field_value
        return updated_data
