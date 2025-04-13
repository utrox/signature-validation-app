from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from core.exceptions.exceptions import BadRequestException, NotFoundException
from documents.models import Document
from signatures.serializers import SignatureSerializer
from signature_workflows.constants import WorkflowStatus
from .models import SignatureWorkflow
from .constants import INCORRECT_WORKFLOW_STATE_ERROR_MESSAGES


class SignatureWorkflowCreateSerializer(serializers.ModelSerializer):
    document_id = serializers.IntegerField()
    form_data = serializers.DictField(required=False)

    class Meta:
        model = SignatureWorkflow
        fields = ["document_id", "form_data"]

    def validate(self, data):
        document_id = data.get("document_id", None)
        form_data = data.get("form_data", None)

        # See N+1 problem in the query.
        # We can use select_related to get the form and prefetch_related to get the form fields.
        # Otherwise an extra query will be made for each form field.
        # See http://docs.djangoproject.com/en/5.2/ref/models/querysets/#prefetch-related
        document = get_object_or_404(
            Document.objects.select_related("form").prefetch_related("form__form_fields"),
            id=document_id
        )

        # Check for form data validity.
        if not form_data and document.requires_form_for_submission:
            raise BadRequestException("Form data is required.")
        elif form_data:
            for field in document.form.form_fields.filter(required=True):
                if field.required and field.field_id not in form_data:
                    raise BadRequestException(f"Field '{field.label}' is required.")

        data["document"] = document
        return data

    def create(self, validated_data):
        return SignatureWorkflow.objects.create(
            document=validated_data["document"],
            user=self.context["request"].user,
            form_data=validated_data.get("form_data") or {}
        )


class SignatureWorkflowHistorySerializer(serializers.Serializer):
    history_date = serializers.DateTimeField()
    history_user = serializers.StringRelatedField()
    history_type = serializers.CharField()
    status = serializers.CharField()

    class Meta:
        fields = ['history_date', 'history_user', 'history_type', 'status']


class SignatureWorkflowListSerializer(serializers.ModelSerializer):
    document_name = serializers.CharField(source='document.name')
    history = serializers.SerializerMethodField()

    class Meta:
        model = SignatureWorkflow
        fields = ['id', 'document_name', 'history', 'status', 'form_data', 'created_at']

    def get_document_name(self, obj):
        return obj.document.name if obj.document else ""
    
    def get_history(self, obj):
        """
        Returns the history of the signature workflow as a list of dictionaries.
        """
        historical_qs = obj.history.all().order_by('-history_date')
        return SignatureWorkflowHistorySerializer(historical_qs, many=True).data


class SignatureVerificationSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    signature_data = serializers.DictField()

    def validate(self, data):
        try:
            workflow = SignatureWorkflow.objects.get(id=data["id"], user=self.context["request"].user)
        except SignatureWorkflow.DoesNotExist:
            raise NotFoundException("Workflow not found.")

        if workflow.status != WorkflowStatus.ACCEPTED_BY_CLERK:
            raise BadRequestException(INCORRECT_WORKFLOW_STATE_ERROR_MESSAGES[workflow.status])

        self.workflow = workflow

        signature_serializer = SignatureSerializer(
            data=data["signature_data"],
            context=self.context
        )

        if not signature_serializer.is_valid():
            raise ValidationError(signature_serializer.errors)

        self.signature_instance = signature_serializer.model_instance()
        return data

    def save(self):
        user = self.context["request"].user
        workflow = self.workflow

        errors = user.profile.verify_signature(self.signature_instance)

        if errors:
            workflow.rejected_signatures += 1
            if workflow.rejected_signatures >= settings.MAX_REJECTED_SIGNATURES:
                workflow.status = WorkflowStatus.REJECTED
            workflow.save()
            raise BadRequestException(errors)

        workflow.status = WorkflowStatus.ACCEPTED
        workflow.save()
        return workflow


class SignatureWorkflowCancelSerializer(serializers.Serializer):
    id = serializers.UUIDField()

    def validate(self, data):
        try:
            workflow = SignatureWorkflow.objects.get(id=data["id"], user=self.context["request"].user)
        except SignatureWorkflow.DoesNotExist:
            raise NotFoundException("Workflow not found.")

        if workflow.status not in [WorkflowStatus.SUBMITTED, WorkflowStatus.ACCEPTED_BY_CLERK]:
            raise BadRequestException("You can only cancel in-progress workflows.")

        self.workflow = workflow
        return data

    def save(self):
        self.workflow.status = WorkflowStatus.CANCELLED
        self.workflow.save()
        return self.workflow
