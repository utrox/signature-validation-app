import { createElement } from "react";
import {
  Edit,
  CheckCircle,
  HourglassEmpty,
  Cancel,
  Close,
  Error,
} from "@mui/icons-material";

export type Order = "asc" | "desc";

export const WORKFLOW_STATUSES = {
  submitted: {
    label: "Awaiting Review",
    icon: createElement(HourglassEmpty, { style: { color: "orange" } }),
    instruction:
      "Your document has been submitted and is awaiting review by a clerk. No action needed from your part yet, kick back and relax.",
  },
  accepted_by_clerk: {
    label: "Awaiting Signature",
    icon: createElement(Edit, { style: { color: "blue" } }),
    instruction:
      "Good news! The clerk approved your submitted document. You need to visit the terminal and sign it to continue.",
  },
  rejected_by_clerk: {
    label: "Rejected by Clerk",
    icon: createElement(Cancel, { style: { color: "red" } }),
    instruction:
      "The clerk rejected your submission. You can check here, or in your email notification for the reason and submit again if needed.",
  },
  accepted: {
    label: "Accepted",
    icon: createElement(CheckCircle, { style: { color: "green" } }),
    instruction:
      "Everything's good! Your signature was validated and the workflow is completed successfully! The document is now available for download.",
  },
  rejected: {
    label: "Rejected by Signature Validation",
    icon: createElement(Error, { style: { color: "red" } }),
    instruction:
      "The signature you submitted didn't match the ones we have on record. After multiple failed attempts, the workflow was rejected. You'll need to start over.",
  },
  cancelled: {
    label: "Cancelled by User",
    icon: createElement(Close, { style: { color: "darkred" } }),
    instruction:
      "You or someone on your behalf cancelled the workflow. Nothing more to do here.",
  },
};

export const HISTORY_MAPPING = {
  "+": "Created",
  "~": "Updated",
  "-": "Deleted",
};

export type WorkflowData = {
  id: string;
  document_name: string;
  status: keyof typeof WORKFLOW_STATUSES;
  created_at: string; // ISO format
  history: WorkflowHistory[];
};

export type WorkflowHistory = {
  history_user: string;
  history_type: keyof typeof HISTORY_MAPPING;
  status: keyof typeof WORKFLOW_STATUSES;
  history_date: string; // ISO format
};
