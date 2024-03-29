from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Paper
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    pass
    

class UserForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['keywords', 'number', 'ja', 'choices']
        labels = {
            'keywords': 'キーワード',
            'number': '論文数',
            'ja': '日本語訳',
            'choices': '取得順',
        }
        widgets = {
            'number': forms.NumberInput(),
            'ja': forms.CheckboxInput(),
            'choices': forms.widgets.Select(attrs={'class': 'select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['number'].widget.attrs.update({
            'min': 1,
            'max': 500,
        })


# class UserForm(forms.Form):
#     keywords = forms.CharField(label='キーワード', max_length=100)
#     number = forms.IntegerField(label='論文数', min_value=1, max_value=500, widget=forms.NumberInput(attrs={'class': 'my-class'}))
#     check = forms.BooleanField(
#         label='日本語訳',
#         required=False
#     )
#     choices = forms.fields.ChoiceField(
#         label='取得順',
#         choices = (
#             ("1", "ヒット率"),
#             ("5", "発行日[新しい順]"),
#             ("6", "発行日[古い順]"),
#             ("2", "公開日[新しい順]"),
#             ("3", "公開日[古い順]"),
#             ("4", "資料名順"),
#         ),
#         widget=forms.widgets.Select(attrs={'class': 'select'})
#     )


class ShapForm(forms.Form):
    target = forms.CharField(label='目的変数')
    feature = forms.CharField(label='説明変数', widget=forms.Textarea(attrs={'rows':5}))
    row_index = forms.IntegerField(label='サンプル行番号', min_value=0, initial=0)
    n_splits = forms.IntegerField(label='KFold分割数', min_value=0, initial=5)

    n_estimators_min = forms.IntegerField(label='平均する決定木の最小値', min_value=1, initial=1)
    n_estimators_max = forms.IntegerField(label='平均する決定木の最大値', min_value=1, initial=10)
    n_estimators_div = forms.IntegerField(label='平均する決定木の分割数', min_value=1, initial=3)
    max_depth_min = forms.IntegerField(label='深さの最小値', min_value=1, initial=1)
    max_depth_max = forms.IntegerField(label='深さの最大値', min_value=1, initial=10)
    max_depth_div = forms.IntegerField(label='深さの分割数', min_value=1, initial=3)
    max_features_min = forms.IntegerField(label='特徴量の最小値', min_value=1, initial=1)
    max_features_max = forms.IntegerField(label='特徴量の最大値', min_value=1, initial=10)
    max_features_div = forms.IntegerField(label='特徴量の分割数', min_value=1, initial=3)

    choices = forms.fields.ChoiceField(
        label='モデル',
        choices = (
            ("0", "ランダムフォレスト"),
            ("1", "線形回帰"),
        ),
        widget=forms.widgets.Select(attrs={'class': 'select'})
    )
