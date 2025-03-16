from rest_framework import serializers
from .models import DocumentForm, FormField


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        ordering = ['order']
        fields = ['id', 'label', 'tooltip', 'field_type', 'required', 'order', 'choices']


class DocumentFormSerializer(serializers.ModelSerializer):
    form_fields = FormFieldSerializer(many=True, read_only=True)
    
    class Meta:
        model = DocumentForm
        fields = ['id', 'document', 'description', 'form_fields']
