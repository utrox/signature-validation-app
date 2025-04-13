from django.contrib import admin
from unfold.admin import ModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import SignatureWorkflow


class SignatureWorkflowAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ("document", "user", "created_at", "status")
    list_filter = ("created_at", "updated_at", "status")
    search_fields = ("document__name", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ["form_data"]

    change_form_template = "signature_workflows/workflow_change_form.html"


admin.site.register(SignatureWorkflow, SignatureWorkflowAdmin)
