from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Doctor.objects.filter(user=self.request.user)
