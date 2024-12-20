from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserChangeForm

# 지정된 메서드의 요청만 허용하도록 하는 데코레이터. 인자는 리스트 형태임.
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # 로그인 처리를 한다. django에서는 이런 유저 인증, 쿠키 및 세션 처리 등등
            # 복잡한 과정을 함수 하나로 처리할 수 있도록 미리 구현해 두었음.
            auth_login(request, form.get_user())
            next_url = request.GET.get("next") or 'index'
            return redirect(next_url)

    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, 'accounts/login.html', context)

# POST 요청만 허용하도록 하는 데코레이터.
# 만약 다른 메서드의 요청이 올 경우 405(Method Not Allowed) 오류를 내보낸다.
@require_POST
def logout(request):
    # request를 까서 쿠키에 session id가 있으면 서버의 session 테이블에서 이를 지우고
    # 쿠키에서 session id도 지워주는 이 과정도 django 내부에 죄다 구현되어 있음.
    auth_logout(request)
    return redirect("index")

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()
    
    context = {"form": form}
    return render(request, "accounts/signup.html", context)

@require_POST
def delete(request):
    if request.user.is_authenticated:
        # django가 로그인 된 user를 auth_user 테이블에서 찾고
        # 이 인스턴스를 request 객체의 user 속성으로 직접 접근할 수 있게 할당해 준다.
        # 즉, 아래와 같이 그냥 delete() 메서드로 직접 DB에서 지우는 게 가능하다는 것이다...
        request.user.delete()
        auth_logout(request)
    return redirect("index")

@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("index")

    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, 'accounts/update.html', context)

@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 비밀번호 변경 시에는 기존 session id로 접근하는
            # user의 정보(session 테이블의 value)가 더 이상 일치하지 않게 되고 해당 세션은 지워짐.
            # 따라서 아래와 같이 하면 비밀번호 변경 후 나온 새로운 정보로 클라이언트와 다시 세션을 연결시킴.
            # 이렇게 하면 비밀번호 변경 후 로그아웃 되는 현상을 막을 수 있음.
            update_session_auth_hash(request, form.user)
            return redirect("index")
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "accounts/change_password.html", context)
