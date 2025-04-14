import { useState } from "react";
import dayjs from "dayjs";
import { Box, Button, Divider, Paper, Typography } from "@mui/material";
import { DeleteOutline, DrawOutlined, History } from "@mui/icons-material";

import { WORKFLOW_STATUSES, WorkflowData, WorkflowHistory } from "./types";
import HistoryModal from "./HistoryModal";
import useDeleteWorkflow from "../../requests/useDeleteWorkflow";
import SignatureModal from "./SignatureModal";
import PreviewWorkflowButton from "./PreviewWorkflowButton";

const IS_PHYSICAL_PLACE = import.meta.env.VITE_PHYSICAL_PLACE === "true";

const ResultsMobileCards = ({ filtered }: { filtered: WorkflowData[] }) => {
  const { mutate: deleteWorkflow, isPending } = useDeleteWorkflow();
  const [openModal, setOpenModal] = useState(false);
  const [selectedHistory, setSelectedHistory] = useState<WorkflowHistory[]>([]);

  const [selectedWorkflow, setSelectedWorkflow] = useState<WorkflowData | null>(
    null
  );

  const handleOpenHistory = (history: WorkflowHistory[]) => {
    setSelectedHistory(history);
    setOpenModal(true);
  };

  return (
    <>
      <Box display="flex" flexDirection="column" gap={2}>
        {filtered.map((wf) => (
          <Paper
            key={wf.id}
            sx={{
              p: 2,
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 2,
              "&:hover": {
                backgroundColor: "rgba(0, 0, 0, 0.005)",
              },
            }}
          >
            <Typography
              variant="subtitle1"
              component="h2"
              sx={{
                gridColumn: "span 2",
              }}
            >
              <strong>{wf.document_name}</strong>
            </Typography>
            <Divider sx={{ gridColumn: "span 2" }} />
            <Typography>Status</Typography>
            <Typography sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              {WORKFLOW_STATUSES[wf.status]?.icon}
              <span>{WORKFLOW_STATUSES[wf.status]?.label}</span>
            </Typography>
            <Divider sx={{ gridColumn: "span 2" }} />
            <Typography>Created:</Typography>
            <Typography>{dayjs(wf.created_at).format("YYYY-MM-DD")}</Typography>
            <Divider sx={{ gridColumn: "span 2" }} />
            <Box
              sx={{
                marginLeft: "auto",
                gridColumn: "span 2",
                display: "flex",
                flexWrap: "wrap",
                gap: 1,
              }}
            >
              {/* Buttons for Signing document, showing history, and deleting workflow. */}
              {wf.status === "accepted_by_clerk" && IS_PHYSICAL_PLACE && (
                <Button
                  variant="outlined"
                  color="success"
                  size="small"
                  sx={{ mr: 1 }}
                  onClick={() => setSelectedWorkflow(wf)}
                  startIcon={<DrawOutlined />}
                >
                  Sign Document
                </Button>
              )}
              {(wf.status === "submitted" ||
                wf.status === "accepted_by_clerk") && (
                <Button
                  variant="outlined"
                  size="small"
                  color="error"
                  onClick={() => deleteWorkflow(wf.id)}
                  endIcon={<DeleteOutline />}
                  loading={isPending}
                >
                  Delete
                </Button>
              )}
              <PreviewWorkflowButton workflow={wf} />
              <Button
                variant="outlined"
                color="primary"
                size="small"
                sx={{ mr: 1 }}
                onClick={() => handleOpenHistory(wf.history)}
                startIcon={<History />}
              >
                History
              </Button>
            </Box>
          </Paper>
        ))}
      </Box>
      <HistoryModal
        open={openModal}
        onClose={() => setOpenModal(false)}
        history={selectedHistory}
      />
      <SignatureModal
        open={!!selectedWorkflow}
        workflowId={selectedWorkflow?.id || ""}
        onClose={() => setSelectedWorkflow(null)}
      />
    </>
  );
};

export default ResultsMobileCards;
