"""djangobootcamp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# auth 추가
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
# index는 대문, blog는 게시판
from main.views import index, blog, posting, UserCreateView, UserCreateDone
# UserCreateView : 게정을 추가하는 View
# UserCreateDone : 계정 생성이 완료된 후에 보여줄 화면을 처리하는 View
# from main.views import 

urlpatterns = [
    path('admin/', admin.site.urls),
    # as_view()를 통해 index.html의 내용을 가져옵니다
    path('', index.as_view(), name='index'),
    # URL:80/blog에 접속하면 blog 페이지 + URL이름은 blog이다
    path('blog/', blog, name='blog'),
    # URL:80/blog/숫자로 접속하면 게시글-세부페이지(posting)
    path('blog/<int:pk>/', posting, name='posting'),
    
    # 인증 URL 3개 추가 
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    path('accounts/register/done/', UserCreateDone.as_view(), name='register_done'),   
]
