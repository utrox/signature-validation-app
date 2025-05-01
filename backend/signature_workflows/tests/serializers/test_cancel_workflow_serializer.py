import uuid
from unittest.mock import MagicMock

from django.test import TestCase
from django.contrib.auth import get_user_model

from documents.models import Document
from signature_workflows.serializer import SignatureWorkflowCancelSerializer
from signature_workflows.models import SignatureWorkflow, WorkflowStatus


User = get_user_model()


class SignatureWorkflowCancelSerializerTests(TestCase):  
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
            status=WorkflowStatus.SUBMITTED  
        )  
      
    def test_validate_valid_data(self):  
        data = {'id': self.workflow.id}  
          
        serializer = SignatureWorkflowCancelSerializer(  
            data=data,  
            context={'request': MagicMock(user=self.user)}  
        )  
        self.assertTrue(serializer.is_valid())  
      
    def test_validate_workflow_not_found(self):  
        data = {'id': uuid.uuid4()}  # Random UUID that doesn't exist  
          
        serializer = SignatureWorkflowCancelSerializer(  
            data=data,  
            context={'request': MagicMock(user=self.user)}  
        )  
          
        with self.assertRaises(Exception) as context:  
            serializer.is_valid()  
            self.assertTrue('Workflow not found' in str(context.exception))  
    
    def test_validate_workflow_not_belong_to_user(self):
        another_user = User.objects.create_user(username='anotheruser', password='password')  
        data = {'id': self.workflow.id}

        serializer = SignatureWorkflowCancelSerializer(
            data=data,
            context={'request': MagicMock(user=another_user)}
        )

        with self.assertRaises(Exception) as context:
            serializer.is_valid()
            self.assertTrue('Workflow does not belong to this user' in str(context.exception))

    def test_validate_incorrect_workflow_state(self):  
        # Change workflow status to something that can't be cancelled  
        self.workflow.status = WorkflowStatus.ACCEPTED  
        self.workflow.save()  
          
        data = {'id': self.workflow.id}  
          
        serializer = SignatureWorkflowCancelSerializer(  
            data=data,  
            context={'request': MagicMock(user=self.user)}  
        )  
          
        with self.assertRaises(Exception) as context:  
            serializer.is_valid()  
            self.assertTrue('can only cancel in-progress workflows' in str(context.exception).lower())  
      
    def test_save(self):  
        data = {'id': self.workflow.id}  
          
        serializer = SignatureWorkflowCancelSerializer(  
            data=data,  
            context={'request': MagicMock(user=self.user)}  
        )  
        serializer.is_valid()  
        result = serializer.save()  
          
        self.assertEqual(result.status, WorkflowStatus.CANCELLED)
