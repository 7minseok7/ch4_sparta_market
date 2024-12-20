from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.urls import reverse

# django의 Model Form을 이용하는 경우
class CustomUserChangeForm(UserChangeForm):
    
    # 쓰고자 하는 모델을 명시한 Meta 클래스를 안에 만들어 줘야 한다.
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 참고로 url의 이름으로부터 url을 찾아가는 게 reverse() 함수다.
        # jinja 템플릿으로 {% url 'URL이름' %} 이런 식으로 쓴 그거 맞다.
        if self.fields.get("password"):
            password_help_text = (
                "비밀번호는 " '<a href="{}">여기</a>에서 변경할 수 있습니다.'
            ).format(f"{reverse('accounts:change_password')}")
            self.fields["password"].help_text = password_help_text