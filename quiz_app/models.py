from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField(verbose_name="題目內容")
    explanation = models.TextField(blank=True, null=True, verbose_name="解析/說明")

    class Meta:
        verbose_name = "題目"
        verbose_name_plural = "題目"

    def __str__(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, verbose_name="所屬題目")
    text = models.CharField(max_length=255, verbose_name="選項內容")
    is_correct = models.BooleanField(default=False, verbose_name="是否為正確答案")

    class Meta:
        verbose_name = "選項"
        verbose_name_plural = "選項"

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="使用者")
    score = models.IntegerField(verbose_name="分數")
    total_questions = models.IntegerField(verbose_name="總題數")
    time_spent = models.IntegerField(verbose_name="耗時(秒)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="測驗時間")

    class Meta:
        verbose_name = "測驗紀錄"
        verbose_name_plural = "測驗紀錄"

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, verbose_name="所屬測驗")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="題目")
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="選擇的選項")
    is_correct = models.BooleanField(verbose_name="是否答對")

    class Meta:
        verbose_name = "作答明細"
        verbose_name_plural = "作答明細"