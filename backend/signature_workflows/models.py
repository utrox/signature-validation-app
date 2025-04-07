import json
import uuid

from django.db import models
from .encoding import PrettyJSONEncoder

WORKFLOW_STATUSES = [
    ('submitted', 'Submitted'),
    ('accepted_by_clerk', 'Accepted by Clerk'), 
    ('rejected_by_clerk', 'Rejected by Clerk'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected by signature validation'),
    ('cancelled', 'Cancelled')
]

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
        choices=WORKFLOW_STATUSES,
        default=WORKFLOW_STATUSES[0][0]
    )
    rejected_signatures = models.IntegerField(default=0)
    form_data = models.JSONField(default=dict, encoder=PrettyJSONEncoder)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SignatureWorkflow for document {self.document.name} by user {self.user.username} on {self.created_at}"
    
    @property
    def _get_preview_data_json(self):
        """
        Returns the form data as a JSON string.
        """
        return json.dumps({"document_id": self.document.id, **self.form_data}, indent=4)
