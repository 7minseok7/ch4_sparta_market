from django.db import models

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

    def __str__(self):
        return self.title
