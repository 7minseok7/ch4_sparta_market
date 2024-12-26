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
    # 상품의 id로 상품을 찾는다. 없으면 404 오류
    good = get_object_or_404(Goods, id=id)
    
    context = {"good": good}
    return render(request, "boards/good_detail.html", context)

# @login_required 데코레이터로 접근을 제한하고 로그인 페이지를 바로 띄울 수 있다.
@login_required
def create(request):
    if request.method == "POST":
        
        form = GoodsForm(request.POST, request.FILES)  # 데이터가 바인딩된 폼을 만든다.
        if form.is_valid():  # form에 있는 데이터들이 전부 유효한지를 확인

            # 작성자 필드를 작성해야 하므로 바로 commit을 하진 않음.
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            
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
    if good.author != request.user:
        return redirect("boards:good_detail", good.id)

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
    # 이것도 django에서 기본적으로 지원하는 것이다.
    if request.user.is_authenticated:  # 이 조건을 사용해서 view 내에 분기 처리를 해볼 수도 있겠다.
        good = get_object_or_404(Goods, id=id)
        if good.author == request.user:
            good.delete()
            return redirect("boards:boards")
    return redirect("boards:good_detail")

@require_POST
def like(request, id):
    if request.user.is_authenticated:
        good = get_object_or_404(Goods, id=id)
        if good.like_users.filter(id=request.user.id).exists():
            good.like_users.remove(request.user)  # 좋아요 취소
        else:
            good.like_users.add(request.user)  # 좋아요 등록

        # form으로 데이터 제출 후 현재 페이지에 그대로 머물기 위해서 추가한 코드
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect("accounts:login")