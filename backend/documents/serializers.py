from rest_framework import serializers
from .models import Document

from form_builder.serializers import DocumentFormSerializer

class DocumentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name']


class DocumentDetailsSerializer(serializers.ModelSerializer):
    form = DocumentFormSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'name', 'form']
