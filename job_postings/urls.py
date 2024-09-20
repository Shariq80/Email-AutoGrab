# job_postings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobPostingListView.as_view(), name='job_posting_list'),
    path('create/', views.JobPostingCreateView.as_view(), name='job_posting_create'),
    path('<int:pk>/', views.JobPostingDetailView.as_view(), name='job_posting_detail'),
    path('<int:pk>/update/', views.JobPostingUpdateView.as_view(), name='job_posting_update'),
    path('<int:pk>/delete/', views.JobPostingDeleteView.as_view(), name='job_posting_delete'),
    path('generate-subject-line/', views.generate_subject_line, name='generate_subject_line'),
    path('<int:pk>/apply/', views.job_application, name='job_application'),
]