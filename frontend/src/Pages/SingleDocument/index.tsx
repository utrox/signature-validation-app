import React from "react";
import Page from "../../components/Page";
import useDocuments from "../../requests/useDocuments";
import { Navigate, useParams } from "react-router-dom";
import useAuth from "../../requests/useAuth";

const SingleDocument = () => {
  const { id } = useParams<{ id: string }>();
  if (!id) {
    window.location.href = "/documents";
    return null;
  }

  const { documents, isLoading } = useDocuments(id);
  const document = documents && documents.length > 0 ? documents[0] : null;
  return <Page title={document?.name}>{document?.name}</Page>;
};

export default SingleDocument;
