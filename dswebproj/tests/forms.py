from django import forms
from django.forms import inlineformset_factory
from .models import Question, Choice, Test

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'isRight']
        labels = {
            'text': 'Resposta',
            'isRight': 'Resposta correta?',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title']
        labels = {
            'title': 'Pergunta'
        }

ChoiceFormSet = inlineformset_factory(Question, Choice, form=ChoiceForm, extra=5, can_delete=False) ##estudar o que isso faz

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'theme']
        labels = {
            'title': 'Título',
            'theme': 'Tema',
        }
        
class QuestionSelectForm(forms.Form):
    question_id = forms.IntegerField(widget=forms.HiddenInput())
    question_title = forms.CharField(disabled=True, required=False)
    selected = forms.BooleanField(required=False)
    weight = forms.IntegerField(min_value=1, required=False)
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super(QuestionSelectForm, self).__init__(*args, **kwargs)
        if question:
            self.fields['question_id'].initial = question.id
            self.fields['question_title'].initial = question.title

QuestionSelectFormSet = forms.formset_factory(QuestionSelectForm, extra=0)
