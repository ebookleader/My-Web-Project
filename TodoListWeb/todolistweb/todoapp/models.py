from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) # 생성날짜
    schedule_date = models.DateTimeField(null=True) # 스케쥴 날짜
    is_completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True) # 완료날짜
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
