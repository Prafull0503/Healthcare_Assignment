from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer
from patients.models import Patient
from doctors.models import Doctor


class MappingCreateView(generics.CreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient')
        doctor_id = request.data.get('doctor')

        
        try:
            patient = Patient.objects.get(
                id=patient_id,
                user=request.user
            )
        except Patient.DoesNotExist:
            return Response(
                {"error": "You are not allowed to use this patient"},
                status=status.HTTP_403_FORBIDDEN
            )

      
        try:
            doctor = Doctor.objects.get(
                id=doctor_id,
                user=request.user
            )
        except Doctor.DoesNotExist:
            return Response(
                {"error": "You are not allowed to use this doctor"},
                status=status.HTTP_403_FORBIDDEN
            )

        if PatientDoctorMapping.objects.filter(
            patient=patient,
            doctor=doctor
        ).exists():
            return Response(
                {"error": "Doctor already assigned to this patient"},
                status=status.HTTP_400_BAD_REQUEST
            )

        mapping = PatientDoctorMapping.objects.create(
            patient=patient,
            doctor=doctor
        )

        serializer = self.get_serializer(mapping)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MappingListView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        )


class PatientDoctorsView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return PatientDoctorMapping.objects.filter(
            patient_id=patient_id,
            patient__user=self.request.user
        )


class MappingDeleteView(generics.DestroyAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__user=self.request.user
        )