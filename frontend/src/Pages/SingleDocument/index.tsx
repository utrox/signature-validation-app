import Page from "../../components/Page";
import { Navigate, useNavigate, useParams } from "react-router-dom";
import { Container, Typography } from "@mui/material";

import DynamicForm from "./DynamicForm";
import useDocumentDetails from "../../requests/useDocumentDetails";
import DocumentInstructions from "./DocumentInstructions";

import { FormState } from "../../types/dynamic_form";
import useSubmitSignatureWorkflow from "../../requests/useSubmitSignatureWorkflow";
import { useEffect } from "react";
import { getCSRFToken } from "../../requests/csrf";
import { toast } from "react-toastify";

const SingleDocument = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { isSuccess, mutate: submitSignatureWorkflow } =
    useSubmitSignatureWorkflow();

  if (!id) {
    window.location.href = "/documents";
    return null;
  }

  const { document: documentData, isLoading } = useDocumentDetails(id);

  if (!isLoading && !documentData) {
    return <Navigate to="/documents" />;
  }

  // Redirect user to see their created workflow after submission (if successful)
  useEffect(() => {
    if (isSuccess) {
      navigate(`/workflows`);
    }
  }, [isSuccess, navigate]);

  const handleSubmitForm = async (formData: FormState) => {
    await submitSignatureWorkflow({
      document_id: id,
      form_data: formData,
    });
  };

  // We're doing it this way, because we want to open a new tab with the preview.
  // TODO: We could (should) also use a modal, but that's a Future Me problem.
  const handlePreviewForm = (formData: FormState) => {
    const form = document.createElement("form");
    form.style.display = "none";
    form.method = "POST";
    form.action = `${import.meta.env.VITE_BACKEND_URL}/api/documents/preview/`;
    form.target = "_blank";

    // Add form fields (document_id, form_data) to the form
    addHiddenField(form, "document_id", id);
    addHiddenField(form, "form_data", JSON.stringify(formData));

    const csrfToken = getCSRFToken();
    if (csrfToken) {
      addHiddenField(form, "csrfmiddlewaretoken", csrfToken);

      document.body.appendChild(form);
      form.submit();
      document.body.removeChild(form);
    } else {
      toast.warn("CSRF token not found. Please log in again.");
    }
  };

  const addHiddenField = (
    form: HTMLFormElement,
    name: string,
    value: string
  ) => {
    const formDataField = document.createElement("input");
    formDataField.type = "hidden";
    formDataField.name = name;
    formDataField.value = value;
    form.appendChild(formDataField);
  };

  return (
    <Page title={documentData?.name}>
      <Container maxWidth="sm">
        <Typography variant="h3">{documentData?.name}</Typography>
        <DocumentInstructions />
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          documentData && (
            <DynamicForm
              formData={documentData}
              onSubmit={handleSubmitForm}
              onPreview={handlePreviewForm}
            />
          )
        )}
      </Container>
    </Page>
  );
};

export default SingleDocument;
