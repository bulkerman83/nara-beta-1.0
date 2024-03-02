from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # 이메일 주소로 사용자를 가져옵니다.
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.add_error('email', "등록되지 않은 이메일 주소입니다.")
            return email
        
        # 회원가입 시 입력한 이메일과 다른지 확인합니다.
        if user.email != email:
            self.add_error('email', "입력한 이메일과 회원가입 시 입력한 이메일이 다릅니다.")
        
        return email