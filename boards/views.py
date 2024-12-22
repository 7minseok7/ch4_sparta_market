from django.shortcuts import render, redirect, get_object_or_404
from .models import Goods
from .forms import GoodsForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

def goods_list(request):
    goods = Goods.objects.all().order_by('-id')
    context = {
        "goods": goods,
    }
    return render(request, 'boards/goods_list.html', context)

def article_detail(request, id):
    # article = Article.objects.get(id=id)
    # 위 코드는 모델에서 데이터를 가져오는 건데 예외처리를 곁들이자면 아래와 같다.
    # 인자로는 모델 클래스, 조건 순으로 넣으면 된다.
    # 이렇게 하면 위와 동일하게 모델에서 objects.get()을 시도하나
    # (조건 등으로 인해) 찾은 것이 없다면 404 오류를 발생시킨다.
    # 비슷한 기능을 하는 함수로 하나를 찾는 get() 대신 여러 개를 찾는 filter()를 사용한
    # get_list_or_404()가 있다.
    good = get_object_or_404(Goods, id=id)
    
    context = {"good": good}
    return render(request, "boards/good_detail.html", context)

# @login_required 데코레이터로 접근을 제한하고 로그인 페이지를 바로 띄울 수 있다.
# 이때 로그인 페이지 다음에 유저가 가려고 한 페이지를 django가 기억해 주며 쿼리스트링에 next로 지정되어 있다.
# 이는 별도 처리를 해주지 않으면 기존의 login() 함수에 지정된 경로로 이동하게 된다.
@login_required
def create(request):
    # title = request.POST.get("title")
    # content = request.POST.get("content")

    # # 새로운 Article 저장
    # article = Article.objects.create(title=title, content=content)
    # return redirect("article_detail", article.id)

    if request.method == "POST":
        # ModelForm을 사용할 경우
        form = GoodsForm(request.POST, request.FILES)  # 데이터가 바인딩된 폼을 만든다.
        if form.is_valid():  # form에 있는 데이터들이 전부 유효한지를 확인
            
            # ArticleForm은 단순 form이 아닌 ModelForm이므로 Model을 알고 있다.
            # 따라서 해당 form 객체의 save() 메서드로 별도의 manager 호출 없이 직접 데이터에 저장하는 것까지 가능하다.
            article = form.save()
            
            # 다른 곳으로 리다이렉트를 하자.
            return redirect("boards:good_detail", article.id)
    else:
        form = GoodsForm()

    context = {"form": form}
    return render(request, 'boards/create.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def update(request, id):

    # ModelForm 사용
    good = get_object_or_404(Goods, id=id)

    if request.method == "POST":
        
        # ModelForm에 instance를 넘겨줄 경우 해당 데이터를 수정하는 방식으로 동작하게 된다.
        # 위의 create 함수의 경우 instance를 넘겨주지 않았고 이 경우 새로 데이터를 생성하는 방식으로 동작한다.
        form = GoodsForm(request.POST, instance=good)
        if form.is_valid():
            good = form.save()
            return redirect("boards:good_detail", good.id)
        
    else:
        form = GoodsForm(instance=good)

    context = {"form": form, "good": good}
    return render(request, "boards/update.html", context)

@require_POST
def delete(request, id):
    # request에는 기본적으로 로그인한 유저의 정보가 들어 있다.
    # 이것도 django에서 기본적으로 지원하는 것이다...
    if request.user.is_authenticated:  # 이 조건을 사용해섯 view 내에 분기 처리를 해볼 수도 있겠다.
        good = get_object_or_404(Goods, id=id)
        good.delete()
    return redirect("boards:boards")
