"""hotel_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from frontend import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from backend.views import activation_sent_view, activate
from backend.forms import  PasswordReset, SetPassword
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('pages/', include('frontend.urls')),
    path('backend/', include('backend.urls')),
    path('search/', views.search, name='search'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='backend/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='backend/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='backend/password_reset_complete.html'), name='password_reset_complete'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('admin/', admin.site.urls),

#     path('reset-password/', auth_views.PasswordResetView.as_view(template_name='backend/password_reset_done.html', 
#       email_template_name='backend/password_reset_email.txt', 
#       success_url = reverse_lazy('backend:password_reset_request'), form_class=PasswordReset), name='password_reset'
#     ),

#    path(
#         'reset/<uidb64>/<token>/',
#         auth_views.PasswordResetConfirmView.as_view(template_name='backend/password_reset_confirm.html',
#         form_class=SetPassword, success_url = reverse_lazy('backend:password_reset_request')), name='password_reset_confirm'
#     ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
