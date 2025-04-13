import Page from "../../components/Page";

import { useEffect, useState } from "react";
import { Container, Typography } from "@mui/material";

import { WorkflowData } from "./types";
import FilterResults from "./FilterResults";
import ResultsMobileCards from "./ResultsMobileCards";
import WorkflowInstructions from "./WorkflowsInstructions";
import useWorkflows from "../../requests/useWorkflows";

export default function AllWorkflows() {
  const { workflows, isLoading } = useWorkflows();
  const [filtered, setFiltered] = useState<WorkflowData[]>([]);

  useEffect(() => {
    if (workflows) setFiltered(workflows);
  }, [workflows]);

  return (
    <Page title="Your Workflows">
      <Container maxWidth="sm">
        <Typography variant="h4" gutterBottom>
          Your Documents
        </Typography>
        <WorkflowInstructions />

        <Typography variant="h5" gutterBottom>
          Your Document Submissions
        </Typography>

        {/* TOOD: better loading component */}
        {isLoading ? (
          <div>Loading...</div>
        ) : (
          <>
            {/* Filters */}
            <FilterResults
              workflows={workflows || []}
              setFiltered={setFiltered}
            />
            <ResultsMobileCards filtered={filtered} />
          </>
        )}
      </Container>
    </Page>
  );
}
