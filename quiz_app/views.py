from django.shortcuts import render, redirect
from .models import Question
import random

def start_quiz(request):
    request.session['total_questions_answered'] = 0
    request.session['correct_answers'] = 0
    request.session['incorrect_answers'] = 0
    request.session['displayed_questions'] = []
    return redirect('get_question')

def get_question(request):
    questions = Question.objects.exclude(id__in=request.session.get('displayed_questions', []))

    if not questions.exists():
        return redirect('summary')

    question = random.choice(questions)
    displayed_questions = request.session.get('displayed_questions', [])
    displayed_questions.append(question.id)
    request.session['displayed_questions'] = displayed_questions
    request.session['current_question_id'] = question.id

    context = {
        'question': question,
        'options': {
            'A': question.option_a,
            'B': question.option_b,
            'C': question.option_c,
            'D': question.option_d,
        }
    }
    return render(request, 'question.html', context)

def submit_answer(request):
    if request.method == 'POST':
        selected_option = request.POST.get('selected_option')
        question_id = request.session.get('current_question_id')

        if not question_id or not selected_option:
            return redirect('get_question')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return redirect('get_question')

        request.session['total_questions_answered'] += 1
        if selected_option == question.correct_option:
            request.session['correct_answers'] += 1
        else:
            request.session['incorrect_answers'] += 1

        if len(request.session.get('displayed_questions', [])) >= Question.objects.count():
            return redirect('summary')

        return redirect('get_question')
    return redirect('get_question')

def session_summary(request):
    summary = {
        'total_questions_answered': request.session.get('total_questions_answered', 0),
        'correct_answers': request.session.get('correct_answers', 0),
        'incorrect_answers': request.session.get('incorrect_answers', 0),
    }
    request.session.flush()
    return render(request, 'summary.html', {'summary': summary})
