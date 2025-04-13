import json
import uuid

from django.db import models
from simple_history.models import HistoricalRecords
from .encoding import PrettyJSONEncoder


class WorkflowStatus(models.TextChoices):
    SUBMITTED = 'submitted', 'Submitted'
    ACCEPTED_BY_CLERK = 'accepted_by_clerk', 'Awaiting Signature'
    REJECTED_BY_CLERK = 'rejected_by_clerk', 'Rejected by Clerk'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected by signature validation'
    CANCELLED = 'cancelled', 'Cancelled'


class SignatureWorkflow(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name="signature",
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="document_signatures"
    )
    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.SUBMITTED
    )
    rejected_signatures = models.IntegerField(default=0)
    form_data = models.JSONField(default=dict, encoder=PrettyJSONEncoder)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"SignatureWorkflow for document {self.document.name} by user {self.user.username} on {self.created_at}"
    
    @property
    def _get_preview_data_json(self):
        """
        Returns the form data as a JSON string.
        """
        return json.dumps({"document_id": self.document.id, **self.form_data}, indent=4)
