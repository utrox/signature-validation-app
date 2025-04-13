import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

import { WORKFLOW_STATUSES } from "./types";

const WorkflowInstructions = () => {
  return (
    <Box
      sx={{
        mb: 4,
        p: 2,
        backgroundColor: "#f5f5f5",
        borderRadius: 2,
        gap: 2,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Typography variant="h6" gutterBottom>
        Understanding Your Workflows
      </Typography>

      <Typography variant="body1">
        This page shows all your active and completed document workflows. Each
        workflow goes through different statuses from submission to final
        resolution. Keep an eye on them to make sure everything moves smoothly.
      </Typography>

      <Typography variant="body1">
        You will get notified about the changes in your workflow instantly as
        they happen, but you can always revisit completed workflows too. You
        will be able to view the current status of your inquery, whether it's
        still in progress, or it was accepted, rejected, or cancelled. Rejected
        workflows will come with a reason, so you’ll know what went wrong and
        how to fix it if needed.
      </Typography>

      <Typography variant="body1">
        Below you'll find a list of possible statuses for your convinience:
      </Typography>

      <List dense>
        {Object.values(WORKFLOW_STATUSES).map((status) => (
          <ListItem
            sx={{ "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.025)" } }}
            key={status.label}
          >
            <ListItemIcon>{status.icon}</ListItemIcon>
            <ListItemText
              primary={status.label}
              secondary={status.instruction}
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default WorkflowInstructions;
