from django import forms
from .models import User

class LoginForm(forms.Form):
	username = forms.CharField(min_length=4)
	password = forms.CharField(min_length=4)


class SignupForm(forms.Form):
	username = forms.CharField(label="아이디")
	password1 = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
	password2 = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")
	short_description = forms.CharField()
	email = forms.EmailField(label="이메일")
	
	def clean_username(self):
		username = self.cleaned_data.get('username')

        # 아이디가 5글자 이상인지 확인
		if len(username) < 6:
			raise forms.ValidationError('아이디는 최소 6글자 이상이어야 합니다.')

		return username

	def clean_password1(self):
		password1 = self.cleaned_data.get('password1')

        # 여기에서 비밀번호에 대한 추가적인 유효성 검사를 수행합니다.
		if not any(char.islower() for char in password1):
			raise forms.ValidationError('비밀번호는 적어도 하나의 소문자를 포함해야 합니다.')

		if len(password1) < 8:
			raise forms.ValidationError('비밀번호는 적어도 영어 소문자 포함 8글자 이상이어야 합니다.')

		if not any(char for char in password1 if char in "!@#$%^&*()_+"):
			raise forms.ValidationError('비밀번호는 특수문자(!@#$%^&*()_+)를 포함해야 합니다.')

		return password1

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')	


class EmailForm(forms.Form):
    email = forms.EmailField(label='이메일')