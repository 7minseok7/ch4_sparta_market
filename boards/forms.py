from django import forms
from .models import Goods

# django의 Model Form을 이용하는 경우
class GoodsForm(forms.ModelForm):
    
    # 쓰고자 하는 모델을 명시한 Meta 클래스를 안에 만들어 줘야 한다.
    class Meta:

        # 먼저 해당 모델 클래스를 준다.
        model = Goods

        # 모든 속성을 이용한 폼을 만들 걱이므로 fields 속성에 "__all__" 을 준다.
        fields = "__all__"
