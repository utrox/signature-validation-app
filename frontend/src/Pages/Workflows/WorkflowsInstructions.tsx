import { WORKFLOW_STATUSES } from "./types";
import InstructionsComponent from "../../components/Instructions";

const WorkflowInstructions = () => {
  const title = "Understanding Your Workflows";
  const bodyTexts = [
    "This page shows all your active and completed document workflows. Each\
      workflow goes through different statuses from submission to final\
      resolution. Keep an eye on them to make sure everything moves smoothly.",
    "You will get notified about the changes in your workflow instantly as\
        they happen, but you can always revisit completed workflows too. You\
        will be able to view the current status of your inquery, whether it's\
        still in progress, or it was accepted, rejected, or cancelled. Rejected\
        workflows will come with a reason, so you’ll know what went wrong and\
        how to fix it if needed.",
    "Below you'll find a list of possible statuses for your convinience:",
  ];
  const listItems = Object.values(WORKFLOW_STATUSES);
  return (
    <InstructionsComponent
      instructionsTitle={title}
      bodyTexts={bodyTexts}
      listItems={listItems}
    />
  );
};

export default WorkflowInstructions;
