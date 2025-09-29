from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('resume/<int:profile_id>/', views.resume_view, name = 'resume_view'),
    path('register/', views.register, name='register'),
    path('resume/<int:profile_id>/download/', views.download_resume, name='download_resume'),
]
