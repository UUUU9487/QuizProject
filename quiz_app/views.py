import random
import time
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, QuizAttempt, UserAnswer

# ==========================================
# 1. 會員登入與註冊系統
# ==========================================
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# ==========================================
# 2. 首頁與測驗核心
# ==========================================
@login_required(login_url='/login/')
def home_view(request):
    if request.method == 'POST':
        num_questions = int(request.POST.get('num_questions', 5))
        mode = request.POST.get('quiz_mode', 'normal')
        
        # 🔥 【加上這兩行終極防呆】
        # 如果從首頁傳來了 practice，我們直接強制把它轉回 normal！
        if mode == 'practice':
            mode = 'normal'
            
        all_ids = list(Question.objects.values_list('id', flat=True))
        # ... 下面維持你原本的程式碼 ...
        all_ids = list(Question.objects.values_list('id', flat=True))
        if not all_ids:
            return render(request, 'start.html', {'error': '題庫目前沒有題目喔！請先至後台新增。'})
            
        if len(all_ids) < num_questions:
            num_questions = len(all_ids)
            
        random.shuffle(all_ids)
        request.session['pool'] = all_ids[:num_questions]
        request.session['target_num'] = num_questions
        request.session['quiz_mode'] = mode
        
        if mode == 'exam':
            time_limit = 600 if num_questions == 5 else 1200
            request.session['exam_end_time'] = time.time() + time_limit
            
        request.session['score'] = 0
        request.session['current_q_num'] = 1
        request.session['mistakes'] = []
        request.session['user_answers'] = []
        request.session['start_time'] = time.time()
        request.session['saved_attempt'] = False
        return redirect('quiz')
    return render(request, 'start.html')

@login_required(login_url='/login/')
def quiz_view(request):
    pool = request.session.get('pool', [])
    if not pool:
        return redirect('result')
        
    mode = request.session.get('quiz_mode', 'practice')
    time_left = 0
    if mode == 'exam':
        time_left = int(request.session.get('exam_end_time', 0) - time.time())
        if time_left <= 0:
            return redirect('result')
            
    current_q_id = pool[0]
    question = Question.objects.get(id=current_q_id)
    choices = list(question.choices.all())
    
    if request.method == 'POST':
        selected_choice_id = request.POST.get('choice')
        if not selected_choice_id:
            return render(request, 'quiz.html', {'question': question, 'choices': choices, 'time_left': time_left, 'error': '請選擇一個答案！'})
            
        selected_choice = Choice.objects.get(id=selected_choice_id)
        is_correct = selected_choice.is_correct
        correct_choice = next((c for c in choices if c.is_correct), None)
        
        user_answers = request.session.get('user_answers', [])
        user_answers.append({'q_id': question.id, 'c_id': selected_choice.id, 'is_correct': is_correct})
        request.session['user_answers'] = user_answers
        
        if is_correct:
            request.session['score'] = request.session.get('score', 0) + 1
        else:
            mistakes = request.session.get('mistakes', [])
            if question.id not in mistakes:
                mistakes.append(question.id)
            request.session['mistakes'] = mistakes
            
        pool.pop(0)
        request.session['pool'] = pool
        request.session['current_q_num'] += 1
        
        return render(request, 'quiz.html', {
            'question': question, 'show_result': True, 'is_correct': is_correct, 
            'correct': correct_choice, 'current_q_num': request.session.get('current_q_num') - 1, 'time_left': time_left
        })
        
    random.shuffle(choices)
    return render(request, 'quiz.html', {'question': question, 'choices': choices, 'show_result': False, 'current_q_num': request.session.get('current_q_num', 1), 'time_left': time_left})

# ==========================================
# 3. 成績結算與補考功能
# ==========================================
@login_required(login_url='/login/')
def result_view(request):
    target_num = request.session.get('target_num', 1)
    score_count = request.session.get('score', 0)
    final_score = int((score_count / target_num) * 100) if target_num > 0 else 0
    mistakes = request.session.get('mistakes', [])
    
    current_mode = request.session.get('quiz_mode', 'normal') 
    
    # 👉 就是少了這一行！告訴 Python 什麼是 is_practice
    is_practice = (current_mode == 'practice')
    
    if not request.session.get('saved_attempt', False):
        if current_mode != 'practice':
            time_spent = int(time.time() - request.session.get('start_time', time.time()))
            attempt = QuizAttempt.objects.create(
                user=request.user, score=final_score, total_questions=target_num, time_spent=time_spent
            )
            user_answers = request.session.get('user_answers', [])
            for ans in user_answers:
                UserAnswer.objects.create(
                    attempt=attempt, question_id=ans['q_id'], selected_choice_id=ans['c_id'], is_correct=ans['is_correct']
                )
        request.session['saved_attempt'] = True

    # 這裡才能順利把 is_practice 傳出去
    return render(request, 'result.html', {
        'score': final_score, 
        'mistakes_count': len(mistakes), 
        'has_mistakes': len(mistakes) > 0, 
        'is_practice': is_practice
    })

@login_required(login_url='/login/')
def retry_mistakes_view(request):
    mistakes = request.session.get('mistakes', [])
    if not mistakes:
        return redirect('home')
        
    request.session['pool'] = mistakes
    request.session['target_num'] = len(mistakes)
    request.session['score'] = 0
    request.session['current_q_num'] = 1
    request.session['mistakes'] = []
    request.session['user_answers'] = []
    request.session['saved_attempt'] = False
    request.session['start_time'] = time.time()
    request.session['quiz_mode'] = 'practice'
    return redirect('quiz')

@login_required(login_url='/login/')
def global_review_quiz(request):
    wrong_answers = UserAnswer.objects.filter(attempt__user=request.user, is_correct=False)
    q_ids = list(wrong_answers.values_list('question_id', flat=True).distinct())
    
    if not q_ids:
        return redirect('review')
        
    random.shuffle(q_ids)
    request.session['pool'] = q_ids[:10]
    request.session['target_num'] = len(request.session['pool'])
    request.session['score'] = 0
    request.session['current_q_num'] = 1
    request.session['mistakes'] = []
    request.session['user_answers'] = []
    request.session['saved_attempt'] = False
    request.session['start_time'] = time.time()
    request.session['quiz_mode'] = 'practice'
    return redirect('quiz')

# ==========================================
# 4. 歷史、排行與錯題紀錄
# ==========================================
@login_required(login_url='/login/')
def history_view(request):
    attempts = QuizAttempt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'attempts': attempts})

@login_required(login_url='/login/')
def history_detail_view(request, attempt_id):
    attempt = QuizAttempt.objects.get(id=attempt_id, user=request.user)
    user_answers = UserAnswer.objects.filter(attempt=attempt)
    return render(request, 'history_detail.html', {'attempt': attempt, 'user_answers': user_answers})

@login_required(login_url='/login/')
def leaderboard_view(request):
    records = QuizAttempt.objects.all().order_by('-score', 'time_spent')[:10]
    return render(request, 'leaderboard.html', {'records': records})

@login_required(login_url='/login/')
def review_view(request):
    wrong_answers = UserAnswer.objects.filter(attempt__user=request.user, is_correct=False)
    unique_mistakes = {}
    for ans in wrong_answers:
        correct_choice = ans.question.choices.filter(is_correct=True).first()
        correct_text = correct_choice.text if correct_choice else "無"
        unique_mistakes[ans.question.id] = {
            'question_text': ans.question.text,
            'user_wrong_choice': ans.selected_choice.text,
            'correct_answer': correct_text
        }
    return render(request, 'review.html', {'mistakes': unique_mistakes.values()})