import "./documents.css";
import React from "react";

import { Container, Typography } from "@mui/material";

import Page from "../../components/Page";
import AllDocumentsInstructions from "./DocumentsInstructions";
import DocumentTable from "./DocumentTable";

const Document: React.FC = () => {
  return (
    <Page title="Documents">
      <Container maxWidth="sm">
        <Typography variant="h4" gutterBottom>
          All Documents
        </Typography>
        <AllDocumentsInstructions />
        <DocumentTable />
      </Container>
    </Page>
  );
};

export default Document;
