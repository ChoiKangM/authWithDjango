# Auth 인증 시스템 구현
> 웹 개발 시 필수 기능인 인증(`Auth`)기능을 만들어봅니다

인증 기능은 일반적으로 로그인 시 username/password를 인증(`authentication`)하는 것 외에도  
로그인한 사용자에 대한 권한(`authorization`)부여까지 포함됩니다.  
장고 엔진 내부에서 웹 요청 및 사용자 식별, 사용자별 세션 할당 및 관리 기능도 수행되는데,  
이런 세션 처리 기능도 인증 기능에 포함됩니다.

내용이 쉽지 않죠?  
똑똑한 장고가 자동으로 만들어주는 부분도 있고,  
프로그래머가 직접 만들어야하는 부분도 있습니다.  
코드로 직접 짜면서 부딪혀봅니다.  

# [기본적인 게시판 만들기](https://github.com/haedal-with-knu/djangoBootcamp/blob/master/dashboard.md) 코드 가져오기

`기본적인 게시판 만들기` 강의에서 만든 코드를 정리해두었습니다  
가져옵니다  
```console
root@goorm:/workspace/djangoBootcamp# git clone https://github.com/kei01138/bootCamp_Week3
```

`bootCamp_Week3` 폴더 내부의 `mysite` 폴더를 `bootCamp_Week3`,`manage.py`와 같은 위치에 있도록 밖으로 꺼냅시다  
`변경 후`
```
.
|-- bootcamp_Week3
    |-- ...
|-- mysite
|-- manage.py
|-- README.md
```
마우스로 왼쪽의 폴더 트리에서 꺼내도 되고,  
리눅스 커맨드를 이용해 꺼내도 됩니다  
```console
root@goorm:/workspace/djangoBootcamp# mv bootCamp_Week3/mysite/ /workspace/djangoBootcamp/mysite
```


## `웹서버 실행` 복습  

**프로젝트를 실행할때마다 반복해서 사용하는 명령어입니다**  
파이썬 가상환경 설정 
```console
root@goorm:/workspace/djangoBootcamp/mysite# source myvenv/bin/activate
```
이제 `django` 웹서버를 실행합시다   
구름 IDE를 사용하는 경우  
상단 메뉴바의 `프로젝트 -> 실행 URL과 포트`에서   
80번 포트를 설정 후 접속합니다
```console
(myvenv) root@goorm:/workspace/djangoBootcamp/mysite# python3 manage.py runserver 0:80 
```

# `settings.py`에서 `URL` 설정
* `LOGIN_URL` : 로그인이 필요해 로그인 페이지로 리다이렉트 시키는 URL로, 디폴트로 `/accounts/login/` URL을 사용합니다
* `LOGOUT_URL` : 로그아웃시 사용하는 URL로, 디폴트로 `/accounts/logout/` URL을 사용합니다
* `LOGIN_REDIRECT_URL` : 로그인 처리가 성공한 후 사용하는 URL로, 디폴트로 `/accounts/profile/` URL을 사용합니다. 우리는 디폴트가 아닌 `/`로 이동합니다

`mysite/djangobootcamp/settings.py`  
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    # django와 static 폴더 연결
    os.path.join(BASE_DIR, 'static'),
)
# 상단 내용 동일

# Django에서 디폴트로 지정된 항목들
# LOGIN_URL = '/accounts/login/'
# LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/
```

# `settings.py`에 설치된 앱 확인
`django` 내부에 설치된 `auth`를 기반으로 인증 시스템을 구현할 예정입니다  
처음 `startproject` 명령에 의해 `settings.py` 설정 파일이 만들어지는데,  
여기에 기본으로 `django.contrib.auth` 앱이 들어 있습니다.  
내부에 설치된 앱을 확인해봅니다    

`mysite/djangobootcamp/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    # 장고 내부 인증 시스템 사용
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # main 어플리케이션 추가
    'main',
]
```

# `Model` 코딩
똑똑한 장고는 인증 기능에 필요한 기본적인 내용을 지원합니다.  
우리는 회원가입 부분과 회원가입 완료 부분만 제작하면 됩니다.  
아래 표에서 마지막 2줄만 직접 제작하면 됩니다

| URL 패턴                        	| 뷰 이름                        	| 템플릿 파일명                                                                                                        	|
|---------------------------------	|--------------------------------	|----------------------------------------------------------------------------------------------------------------------	|
| /accounts/login/                	| login()                        	| registration/login.html                                                                                              	|
| /accounts/logout/               	| logout()                       	| registration/logged_out.html                                                                                         	|
| (개발자가 지정)                 	| logout_then_logout()           	| (개발자가 지정)                                                                                                      	|
| /accounts/passward_change/      	| password_change()              	| registration/password_change_form.html                                                                               	|
| /accounts/password_change/done/ 	| password_change_done()         	| registration/password_change_done.html                                                                               	|
| /accounts/password_reset/       	| password_reset()               	| registration/password_reset_form.html registration/password_reset_email.html registration/password_reset_subject.txt 	|
| /accounts/password_reset/done/  	| password_reset_done()          	| registration/password_reset_done.html                                                                                	|
| /accounts/reset/                	| password_reset_confirm()       	| registration/password_reset_confirm.html                                                                             	|
| /accounts/reset/done/           	| password_reset_complete()      	| registration/password_reset_complete.html                                                                            	|
| /accounts/register/             	| UserCreateView(CreateView)     	| registration/register.html                                                                                           	|
| /accounts/register/done/        	| UserCreateDoneTV(TemplateView) 	| registration/register_done.html                                                                                      	|



