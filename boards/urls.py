from django.urls import path
from . import views

app_name = "boards"
urlpatterns = [
    path("", views.goods_list, name="boards"),

    path("create/", views.create, name="create"),
    path("<int:id>/", views.article_detail, name="good_detail"),
    path("<int:id>/delete/", views.delete, name="delete"),
    path("<int:id>/update/", views.update, name="update"),
]
