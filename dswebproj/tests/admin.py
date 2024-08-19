from django.contrib import admin

from .models import Question, Choice, Test, TestQuestionWeight

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('title',)

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
admin.site.register(Test)
admin.site.register(TestQuestionWeight)
