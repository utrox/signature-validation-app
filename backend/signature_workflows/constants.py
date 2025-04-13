from .models import SignatureWorkflow, WorkflowStatus

INCORRECT_WORKFLOW_STATE_ERROR_MESSAGES = {
    WorkflowStatus.SUBMITTED: "Document is waiting for review by a clerk.",
    WorkflowStatus.REJECTED_BY_CLERK: "Document was rejected by clerk, it cannot be signed.",
    WorkflowStatus.ACCEPTED: "Document is already signed, you cannot submit more signatures.",
    WorkflowStatus.REJECTED: "Document's already been rejected by invalid signatures.",
    WorkflowStatus.CANCELLED: "Document's been already cancelled.",
}