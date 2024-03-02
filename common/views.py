from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from common.forms import LoginForm, SignupForm

from .models import User
from pybo.models import Advertisement
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from .forms import EmailForm

from django.http import HttpResponse


def mypage(request):
    user = request.user
    advertisement_first = Advertisement.objects.all()[0]
    advertisement_second = Advertisement.objects.all()[1]
    advertisement_last = Advertisement.objects.all()[2]
    context = {'user':user, 'advertisement_first':advertisement_first, 'advertisement_second':advertisement_second, 'advertisement_last':advertisement_last,}
    return render(request, 'common/mypage.html', context)

def login_view(request):
	if request.user.is_authenticated:
		return redirect('pybo:index')
	

	if request.method == "POST":
		form = LoginForm(data=request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			remember_me = request.POST.get('remember_me')

			user = authenticate(username=username, password=password)

			response=redirect('pybo:index')

			if user:
				login(request, user)
				if remember_me:
					response.set_cookie('username', username)
					response.set_cookie('remember_me', 'checked')
				else:
					response.delete_cookie('username')
					response.delete_cookie('remember_me')
				return response

			else:
				form.add_error(None, "아이디 또는 비밀번호를 다시 확인하세요!")
				
		context = {"form":form}
		return render(request, "common/login.html", context)

	else:
		form=LoginForm()
		username = request.COOKIES.get('username','')
		remember_me_checked = request.COOKIES.get('remember_me', '')
		context={"form":form, "username":username, 'remember_me_checked': remember_me_checked}
		return render(request, "common/login.html", context)



def logout_view(request):
	logout(request)
	return redirect('common:login')


def signup(request):
	if request.method == "POST":
		form = SignupForm(data=request.POST)
		if form.is_valid():
			username= form.cleaned_data["username"]
			password1 = form.cleaned_data["password1"]
			password2 = form.cleaned_data["password2"]
			short_description = form.cleaned_data["short_description"]
			email = form.cleaned_data["email"]

			if password1 != password2:
				form.add_error("password2", "비밀번호를 다시 확인해 주세요")

			if User.objects.filter(username=username).exists():
				form.add_error("username", "입력한 ID는 이미 사용중 입니다")

			if User.objects.filter(email=email).exists():
				form.add_error("email", "이미 사용중인 이메일 입니다")

			if form.errors:
				context = {"form":form}
				return render(request, "common/signup.html", context)

			else:

				user = User.objects.create_user(
					username=username,
					password=password1,
					short_description=short_description,
					email=email,
					is_active=False,
					)

				
				return send_verification_email(request, user)

		return render(request, "common/signup.html", {"form":form})

	else:
		form = SignupForm()
		context = {"form":form}
		return render(request, "common/signup.html", context)



def send_verification_email(request, user):
    code = get_random_string(6)  # 무작위 6자리 코드 생성
    request.session['code'] = code
    request.session['user_id'] = user.id


    subject = '회원가입 인증 코드'
    message = f'회원가입 인증 코드: {code}'
    from_email = 'bulkerman83@naver.com'
    recipient_list = [user.email]
    
    send_result = send_mail(subject, message, from_email, recipient_list)
    if send_result:
	    return redirect('common:verification')
    else:
        return HttpResponse("이메일 발송실패")


def verification(request):
    if request.method == 'POST':
        session_code = request.session['code']
        code = request.POST.get('verification_code')
        if session_code == code:
            user=User.objects.get(id=request.session['user_id'])
            user.is_active=True
            user.save()
            del request.session['code']
            del request.session['user_id']
            login(request, user)
            return redirect('pybo:index')  # 홈 페이지 또는 원하는 페이지로 리디렉션
        else:
            user=User.objects.get(id=request.session['user_id'])
            user.delete()
            return render(request, 'common/verification_fail.html')
    return render(request, 'common/verification.html')


def find_username_by_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                username = user.username
                return render(request, 'common/username.html', {'username': username})
            except User.DoesNotExist:
                return render(request, 'common/username.html', {'error_message': '해당 이메일로 등록된 사용자가 없습니다.'})
    else:
        form = EmailForm()
    return render(request, 'common/email_form.html', {'form': form})




from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
import re

class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm

    def form_valid(self, form):
        password1 = form.cleaned_data.get('new_password1')
        password2 = form.cleaned_data.get('new_password2')

        min_length = 8

        if password1 and len(password1) < min_length:
            form.add_error('new_password1', f'비밀번호는 최소 {min_length}자 이상이어야 합니다.')
            return self.form_invalid(form)

        if password1 and password2 and password1 != password2:
            form.add_error('new_password2', '비밀번호가 일치하지 않습니다.')
            return self.form_invalid(form)

        if not re.search(r'[a-z]', str(password1)):
            form.add_error('new_password1', '비밀번호에는 영어 소문자가 반드시 포함되어야 합니다.')
            return self.form_invalid(form)

        return super().form_valid(form)