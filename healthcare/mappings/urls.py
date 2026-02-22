from django.urls import path
from .views import (
    MappingCreateView,
    MappingListView,
    PatientDoctorsView,
    MappingDeleteView
)

urlpatterns = [
    path('', MappingListView.as_view(), name='mapping-list'),
    path('create/', MappingCreateView.as_view(), name='mapping-create'),
    path('<int:patient_id>/', PatientDoctorsView.as_view(), name='patient-doctors'),
    path('delete/<int:pk>/', MappingDeleteView.as_view(), name='mapping-delete'),
]
