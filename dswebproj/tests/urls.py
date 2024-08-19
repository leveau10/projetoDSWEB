from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name='tests'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register-question/', views.register_question, name='register_question'),
    path('list-tests/<int:theme_id>', views.list_tests, name='list_tests'),
    path('test-details/<int:test_id>', views.test_details, name='test_details'),
    path('register-test/', views.create_test, name='create_test'),
]