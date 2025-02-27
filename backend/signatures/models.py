import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


DOCUMENT_SIGNATURE_STATUES = [
    ('submitted', 'Submitted'),
    ('accepted_by_clerk', 'Accepted by Clerk'), 
    ('rejected_by_clerk', 'Rejected by Clerk'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled')
]

class Signature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="signatures")
    file = models.FileField(upload_to='signatures/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_sec = models.IntegerField() # Reject signatures that took too long


class DocumentSignProcess(models.Model):
    document = models.OneToOneField(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name="signature",
        primary_key=True
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="document_signatures"
    )
    status = models.CharField(
        max_length=20,
        choices=DOCUMENT_SIGNATURE_STATUES,
        default=DOCUMENT_SIGNATURE_STATUES[0][0]
    )
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    rejected_signatures = models.IntegerField(default=0)
