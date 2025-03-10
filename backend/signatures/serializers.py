import uuid
import base64
import pickle
import numpy as np

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Signature
from . import encoder

class SignatureSerializer(serializers.Serializer):
    imgData = serializers.CharField()
    signatureTimeMs = serializers.IntegerField()

    class Meta:
        model = Signature
        fields = ['imgData', 'signatureTimeMs', 'file', 'features', 'time_ms']
        read_only_fields = ['file', 'features', 'time_ms']

    def validate_imgData(self, value):
        """Ensure imgData is a valid Base64 string, and decodes it to bytes."""
        try:
            # Split removes the 'data:image/png;base64, <actual base64>' metadata
            # from the beginning of the base64 string.
            decoded_bytes = base64.b64decode(value.split(",")[1], validate=True)
        except Exception:
            raise serializers.ValidationError("Invalid Base64-encoded image data.")
        return decoded_bytes

    def create(self, validated_data):
        img_bytes = validated_data.pop('imgData')
        time_ms = validated_data.pop('signatureTimeMs')

        # TODO: this is where feature extraction will happen.
        signature_img = encoder.preprocess_image(img_bytes)
        features = encoder.extract_features(signature_img)
        features_pickle = pickle.dumps(features)

        # Create a FileField from the base64 string
        file_name = f"signature_{uuid.uuid4()}.png"
        signature_file = ContentFile(img_bytes, name=file_name)

        # Save Signature instance
        return Signature.objects.create(
            user=self.context['request'].user,
            file=signature_file,
            features=features_pickle,
            time_ms=time_ms
        )
