import { Visibility } from "@mui/icons-material";
import { Button } from "@mui/material";
import React from "react";
import { WorkflowData } from "./types";
import { addHiddenField } from "../../utils";
import { getCSRFToken } from "../../requests/csrf";
import { toast } from "react-toastify";

interface PreviewWorkflowButtonProps {
  workflow: WorkflowData;
}

const PreviewWorkflowButton: React.FC<PreviewWorkflowButtonProps> = ({
  workflow,
}) => {
  const handlePreview = () => {
    // We're doing it this way, because we want to open a new tab with the preview.
    // The preview requires us to send the data through POST body for privacy reasons.
    const form = document.createElement("form");
    form.style.display = "none";
    form.method = "POST";
    form.action = `${import.meta.env.VITE_BACKEND_URL}/api/documents/preview/`;
    form.target = "_blank";

    const csrfToken = getCSRFToken();
    addHiddenField(form, "workflow_id", workflow.id);

    if (csrfToken) {
      addHiddenField(form, "csrfmiddlewaretoken", csrfToken);

      document.body.appendChild(form);
      form.submit();
      document.body.removeChild(form);
    } else {
      toast.warn("CSRF token not found. Please log in again.");
    }
  };

  return (
    <Button
      variant="outlined"
      color="secondary"
      size="small"
      onClick={handlePreview}
      startIcon={<Visibility />}
    >
      {workflow.status === "accepted" ? "View" : "Preview"}
    </Button>
  );
};

export default PreviewWorkflowButton;
