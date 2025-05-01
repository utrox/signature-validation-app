import uuid
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.contrib.auth import get_user_model

from signature_workflows.serializer import SignatureVerificationSerializer
from signature_workflows.models import SignatureWorkflow, WorkflowStatus
from documents.models import Document
from signatures.models import Signature


User = get_user_model()
BASE_64_IMG_STRING = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCA1LjEuMvu8A7YAAAC2ZVhJZklJKgAIAAAABQAaAQUAAQAAAEoAAAAbAQUAAQAAAFIAAAAoAQMAAQAAAAIAAAAxAQIAEAAAAFoAAABphwQAAQAAAGoAAAAAAAAAYAAAAAEAAABgAAAAAQAAAFBhaW50Lk5FVCA1LjEuMgADAACQBwAEAAAAMDIzMAGgAwABAAAAAQAAAAWgBAABAAAAlAAAAAAAAAACAAEAAgAEAAAAUjk4AAIABwAEAAAAMDEwMAAAAADp1fY4ytpsegAAADVJREFUOE9jGAU4wX8oDQPofDhggtJkg4E3YHABnCGNBlDUDXwgMkJpECDWCyCArG9AAQMDAGtYBQhykQLeAAAAAElFTkSuQmCC"


class SignatureVerificationSerializerTests(TestCase):  
    def setUp(self):  
        self.user = User.objects.create_user(username='testuser', password='password')  
        self.document = Document.objects.create(  
            name='Test Document',  
            template='document_templates/test.html',  
            is_active=True  
        )  
        self.workflow = SignatureWorkflow.objects.create(  
            document=self.document,  
            user=self.user,  
            form_data={'field1': 'value1'},  
            status=WorkflowStatus.ACCEPTED_BY_CLERK  
        )  
          
    def test_validate_valid_data(self):
        """Test data validation for valid input"""
        data = {  
            'id': self.workflow.id,  
            'signature_data': {  
                'imgData': BASE_64_IMG_STRING,  
                'signatureTimeMs': 1000  
            }  
        }  
          
        # Mock the SignatureSerializer, as we are not testing it here
        with patch('signatures.serializers.SignatureSerializer') as mock_sig_serializer:  
            mock_instance = MagicMock()  
            mock_sig_serializer.return_value = mock_instance  
            mock_instance.is_valid.return_value = True  
            mock_instance.model_instance.return_value = MagicMock(spec=Signature)  
              
            serializer = SignatureVerificationSerializer(  
                data=data,  
                context={'request': MagicMock(user=self.user)}  
            )  
            self.assertTrue(serializer.is_valid())  
      
    def test_validate_workflow_not_found(self):  
        """Test data validation for workflow not found"""
        data = {  
            'id': uuid.uuid4(),  # Random UUID that doesn't exist  
            'signature_data': {  
                'imgData': BASE_64_IMG_STRING,  
                'signatureTimeMs': 1000  
            }  
        }  
          
        serializer = SignatureVerificationSerializer(  
            data=data,  
            context={'request': MagicMock(user=self.user)}  
        )  
          
        with self.assertRaises(Exception) as context:  
            serializer.is_valid()  
            self.assertTrue('Workflow not found' in str(context.exception))  
      
    def test_validate_incorrect_workflow_state(self):  
        """Test data validation for unaccepted (anything other than ACCEPTED_BY_CLERK) workflow state"""
        # We change the workflow status to something other than ACCEPTED_BY_CLERK  
        self.workflow.status = WorkflowStatus.SUBMITTED  
        self.workflow.save()  
          
        data = {  
            'id': self.workflow.id,  
            'signature_data': {  
                'imgData': BASE_64_IMG_STRING,  
                'signatureTimeMs': 1000  
            }  
        }  
          
        serializer = SignatureVerificationSerializer(  
            data=data,  
            context={'request': MagicMock(user=self.user)}  
        )  
          
        with self.assertRaises(Exception) as context:  
            serializer.is_valid()  
            self.assertTrue('incorrect workflow state' in str(context.exception).lower())  
