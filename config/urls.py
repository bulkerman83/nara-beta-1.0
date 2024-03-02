from django.contrib import admin
from django.urls import path, include
from pybo.views import base_views

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

from common.views import CustomPasswordResetView
from .forms import CustomPasswordResetForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')),
    path('', base_views.index, name='index'),  # '/' 에 해당되는 path


    # 비밀번호 재설정 관련
    path('reset_password/', 
         CustomPasswordResetView.as_view(template_name="accounts/password_reset.html", form_class=CustomPasswordResetForm), 
         name="reset_password"),
    path('reset_password_sent/', 
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
         name="password_reset_confirm"),
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
         name="password_reset_complete"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)