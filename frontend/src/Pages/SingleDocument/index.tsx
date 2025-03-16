import Page from "../../components/Page";
import { Navigate, useParams } from "react-router-dom";
import { Container } from "@mui/material";

import DynamicForm from "./DynamicForm";
import useDocumentDetails from "../../requests/useDocumentDetails";
import { FormState } from "../../types/dynamic_form";

const SingleDocument = () => {
  const { id } = useParams<{ id: string }>();
  if (!id) {
    window.location.href = "/documents";
    return null;
  }

  const { document, isLoading } = useDocumentDetails(id);

  if (!isLoading && !document) {
    return <Navigate to="/documents" />;
  }

  const handleSubmitForm = (formData: FormState) => {
    console.log(formData);
  };

  return (
    <Page title={document?.name}>
      <Container maxWidth="sm">
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          document && (
            <DynamicForm formData={document} onSubmit={handleSubmitForm} />
          )
        )}
      </Container>
    </Page>
  );
};

export default SingleDocument;
