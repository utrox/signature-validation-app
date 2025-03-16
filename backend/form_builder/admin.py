from django.contrib import admin
from django.contrib.postgres.fields import ArrayField

from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.forms.widgets import ArrayWidget

from .models import DocumentForm, FormField


class FieldInline(StackedInline):
    model = FormField
    extra = 0
    show_change_link = True

    # Allows for ordering by dragging on the UI.
    ordering_field = "order"
    hide_ordering_field = True

    formfield_overrides = {
        ArrayField: {
            "widget": ArrayWidget,
        }
    }

@admin.register(DocumentForm)
class FormAdmin(ModelAdmin):
    inlines = [FieldInline]

    class Media:
        css = {
            'all': ('admin/css/form_builder.css',)  # Include custom CSS
        }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('form_fields')
