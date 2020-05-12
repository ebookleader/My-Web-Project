from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100) # 제목
    created = models.DateTimeField(auto_now_add=True) # 생성날짜
    schedule_date = models.DateTimeField(null=True) # 스케쥴 날짜
    is_completed = models.BooleanField(default=False) # 완료 boolean 값
    date_completed = models.DateTimeField(null=True, blank=True) # 완료날짜
    important = models.BooleanField(default=False) # 중요 여부
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 사용자

    def __str__(self):
        return self.title
