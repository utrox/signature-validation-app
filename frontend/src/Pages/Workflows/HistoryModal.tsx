// src/components/HistoryModal.tsx
import {
  Dialog,
  DialogTitle,
  DialogContent,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import dayjs from "dayjs";
import { WorkflowHistory, WORKFLOW_STATUSES, HISTORY_MAPPING } from "./types";

interface HistoryModalProps {
  open: boolean;
  onClose: () => void;
  history: WorkflowHistory[];
};

// + for create, ~ for update, and - for delete
// https://django-simple-history.readthedocs.io/en/latest/quick_start.html#what-is-django-simple-history-doing-behind-the-scenes:~:text=history_type%3A%20%2B%20for%20create%2C%20~%20for%20update%2C%20and%20%2D%20for%20delete
const HistoryModal = ({ open, onClose, history }: HistoryModalProps) => {
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Workflow History</DialogTitle>
      <DialogContent>
        <List>
          {history.map((item, idx) => (
            <ListItem key={idx} divider>
              <ListItemText
                primary={`${WORKFLOW_STATUSES[item.status]?.label}`}
                secondary={`${HISTORY_MAPPING[item.history_type]} on ${dayjs(
                  item.history_date
                ).format("YYYY-MM-DD HH:mm")}`}
              />
            </ListItem>
          ))}
        </List>
      </DialogContent>
    </Dialog>
  );
};

export default HistoryModal;
