from django.db import models
from django.conf import settings

# Create your models here.
class Goods(models.Model):
    
    # 데이터 필드 및 형식 지정. (SQL 같이 생각하면 됨)
    title = models.CharField(max_length=50)
    content = models.TextField()

    # 각각 최초 생성일시, 최근 수정일시
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 이미지 업로드 기능
    image = models.ImageField(upload_to="images/", blank=True)

    # 게시글 작성자
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goods"
    )

    # 좋아요 기능 관련 필드
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_goods"
    )

    def __str__(self):
        return self.title
