# challenges/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('problems/', views.show_problems, name='show_problems'),
]


#challenges/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Built-in logout view
    # Other URL patterns
]


urlpatterns = [
    path('problems/', views.problem_list, name='problem_list'),
    path('problems/<int:pk>/', views.problem_detail, name='problem_detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('submit/', views.submit_code, name='submit_code'),
]
# challenges/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submit_code/', views.submit_code, name='submit_code'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('submission_result/<int:submission_id>/', views.submission_result, name='submission_result'),
]

from django.urls import path
from . import views

urlpatterns = [
    path("submit/", views.handle_submission, name="handle_submission"),
]
from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.handle_submission, name='handle_submission'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
