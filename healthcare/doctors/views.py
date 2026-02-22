from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # sirf logged-in user ke doctors
        return Doctor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # doctor ka owner logged-in user hoga
        serializer.save(user=self.request.user)


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user sirf apna doctor hi access kare
        return Doctor.objects.filter(user=self.request.user)