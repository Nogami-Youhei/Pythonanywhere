from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    pass
    

class UserForm(forms.Form):
    keywords = forms.CharField(label='キーワード', max_length=100)
    number = forms.IntegerField(label='論文数', min_value=1, max_value=500, widget=forms.NumberInput(attrs={'class': 'my-class'}))
    check = forms.BooleanField(
        label='日本語訳',
        required=False
    )
    choices = forms.fields.ChoiceField(
        label='取得順',
        choices = (
            ("1", "ヒット率"),
            ("5", "発行日[新しい順]"),
            ("6", "発行日[古い順]"),
            ("2", "公開日[新しい順]"),
            ("3", "公開日[古い順]"),
            ("4", "資料名順"),
        ),
        widget=forms.widgets.Select(attrs={'class': 'select'})
    )
