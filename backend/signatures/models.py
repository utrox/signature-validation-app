import uuid
import pickle
from django.db import models
from django.contrib.auth import get_user_model

from . import encoder


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
    # In a production environment I'd consider leaving this field out.
    # For the demo purposes though, we will have it.
    file = models.FileField(upload_to='uploads/signature_files/')
    features = models.BinaryField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    time_ms = models.IntegerField() # Reject signatures that took too long

    def compare_signature(self, other: 'Signature') -> float:
        features1 = pickle.loads(self.features)
        features2 = pickle.loads(other.features)
        return encoder.compare_features(features1, features2)[0][0] 


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
