from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import QuestionForm, ChoiceFormSet, TestForm, QuestionSelectFormSet
from .models import Test, Choice, TestQuestionWeight, Question

def home(request):
    return render(request, 'tests/home.html')

@login_required()
def profile(request):
    return render(request, 'tests/profile.html')

def register_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST, instance=form.instance)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'Questão cadastrada')
            return redirect('tests:register_question') 
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()

    context = {
        'form': form, 
        'formset': formset
        }

    return render(request, 'tests/register-question.html', context)

def list_tests(request, theme_id):
    if theme_id<1 or theme_id> 5:
        tests = Test.objects.all()
    else:
        tests = Test.objects.filter(theme=theme_id)
    context = {
        'tests': tests,
        'tema': theme_id
    }

    return render(request, 'tests/list-tests.html', context )

def test_details(request, test_id):
    if request.method == 'POST':
        test = get_object_or_404(Test, pk=test_id)
        test_weight = 0
        partial_weight = 0
        selected_choices_ids = []
        for question in test.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            selected_choice = get_object_or_404(Choice, pk=selected_choice_id)


            selected_choices_ids.append(selected_choice_id)


            test_question_weight = TestQuestionWeight.objects.get(test=test, question = question)
            test_weight += test_question_weight.weight
            # Check if the selected choice is correct
            if selected_choice.isRight:
                # Find the weight for this question in the TestQuestionWeight model
                partial_weight += test_question_weight.weight
                    
        nota = partial_weight/test_weight
        nota = nota*100
        # You can store the result or do something else with total_weight
        # For example, redirect to a results page
        selected_choices_queryset = Choice.objects.filter(id__in=selected_choices_ids)
        context = {
            'test': test,
            'nota': int(nota),
            'selected_choices': selected_choices_queryset
        }
    else:
        test = get_object_or_404(Test.objects.prefetch_related('questions', 'questions__choices' ), pk=test_id)
        context = {
            'test': test
        }
    return render(request, 'tests/test-details.html', context)
    
    
def create_test(request):
    questions = Question.objects.all()
    
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        question_formset = QuestionSelectFormSet(request.POST)
        
        if test_form.is_valid() and question_formset.is_valid():
            test = test_form.save()

            for form in question_formset:
                if form.cleaned_data.get('selected'):
                    question_id = form.cleaned_data.get('question_id')
                    weight = form.cleaned_data.get('weight')
                    question = Question.objects.get(id=question_id)
                    test.questions.add(question)
                    TestQuestionWeight.objects.create(test=test, question=question, weight=weight)
            return redirect('tests:list_tests 6')  # Replace with the appropriate success URL
    else:
        test_form = TestForm()
        initial_data = [{'question': q, 'question_id': q.id, 'question_title': q.title} for q in questions]
        question_formset = QuestionSelectFormSet(initial=initial_data)

    return render(request, 'tests/register-test.html', {
        'test_form': test_form,
        'question_formset': question_formset,
    })