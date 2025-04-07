import pickle
from django.db import models
from django.contrib.auth import get_user_model

from . import encoder

User = get_user_model()


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
