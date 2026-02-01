from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset
from .utils import analyze_csv
from django.http import FileResponse
from .pdf_utils import generate_report
from rest_framework.permissions import AllowAny


class CSVUploadView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        summary = analyze_csv(file)

        dataset = Dataset.objects.create(
            file_name=file.name,
            summary=summary
        )

        # Keep only last 5 datasets
        datasets = Dataset.objects.order_by('-uploaded_at')
        if datasets.count() > 5:
            for old in datasets[5:]:
                old.delete()

        return Response(
            {
                "message": "File uploaded successfully",
                "dataset_id": dataset.id,
                "summary": summary
            },
            status=status.HTTP_201_CREATED
        )
from django.shortcuts import get_object_or_404

class SummaryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)

        return Response({
            "dataset_id": dataset.id,
            "file_name": dataset.file_name,
            "uploaded_at": dataset.uploaded_at,
            "summary": dataset.summary
        })
class HistoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        datasets = Dataset.objects.order_by('-uploaded_at')[:5]

        data = []
        for dataset in datasets:
            data.append({
                "dataset_id": dataset.id,
                "file_name": dataset.file_name,
                "uploaded_at": dataset.uploaded_at,
                "summary": dataset.summary
            })

        return Response(data)
class PDFReportView(APIView):
    def get(self, request, dataset_id):
        dataset = get_object_or_404(Dataset, id=dataset_id)

        pdf_buffer = generate_report(dataset)

        return FileResponse(
            pdf_buffer,
            as_attachment=True,
            filename=f"dataset_{dataset_id}_report.pdf"
        )
