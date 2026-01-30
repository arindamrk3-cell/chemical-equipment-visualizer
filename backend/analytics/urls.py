from django.urls import path
from .views import CSVUploadView,SummaryView

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('summary/<int:dataset_id>/', SummaryView.as_view(), name='summary'),
]
