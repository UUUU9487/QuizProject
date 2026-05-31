from django.contrib import admin
from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Question, Choice, QuizAttempt, UserAnswer

class ChoiceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        count = sum(1 for form in self.forms if form.cleaned_data.get('is_correct'))
        if count == 0:
            raise forms.ValidationError("請至少勾選一個正確答案！")

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    can_delete = True
    formset = ChoiceFormSet

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['text'] # 移除了難易度顯示

admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)