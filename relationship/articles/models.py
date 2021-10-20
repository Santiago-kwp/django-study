from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # comment_set 이라는 컬럼이 역참조로 생김 1:N에서 1이 가지고 있는 N을 모두 가져올 수 있음

class Comment(models.Model):
    content = models.CharField(max_length=100)
    article = models.ForeignKey(Article, on_delete=models.CASCADE) # article instance를 저장
    # article_id # 숫자 하나만 저장