from django.contrib import admin
from django.urls import path
from quiz_app import views  # 🔥 關鍵修正：明確告訴系統去 quiz_app 找 views

urlpatterns = [
    # 記得保留管理員後台
    path('admin/', admin.site.urls),
    
    # 會員與首頁
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # 測驗核心功能
    path('quiz/', views.quiz_view, name='quiz'),
    path('result/', views.result_view, name='result'),
    path('retry/', views.retry_mistakes_view, name='retry'),
    path('review-quiz/', views.global_review_quiz, name='review_quiz'),
    
    # 進階功能
    path('history/', views.history_view, name='history'),
    path('history/<int:attempt_id>/', views.history_detail_view, name='history_detail'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('review/', views.review_view, name='review'),
]