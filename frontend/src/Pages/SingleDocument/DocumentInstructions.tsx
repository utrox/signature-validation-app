import ElectricBoltIcon from "@mui/icons-material/ElectricBolt";
import Lock from "@mui/icons-material/Lock";
import GradingIcon from "@mui/icons-material/Grading";
import DoneAllIcon from "@mui/icons-material/DoneAll";
import InstructionsComponent from "../../components/Instructions";

const DocumentInstructions = () => {
  const instructionsTitle = "Before you begin...";
  const bodyTexts = [
    "Please complete the following information related to this document.",
  ];
  const listItems = [
    {
      icon: <ElectricBoltIcon style={{ color: "orange" }} />,
      label:
        "The data you enter here will help us generate your document with lightning speed.",
    },
    {
      icon: <Lock color="primary" />,
      label: "All information will be securely stored.",
    },
    {
      icon: <GradingIcon color="secondary" />,
      label:
        "Entries will be reviewed by a clerk prior to final approval, so please make sure they are in accordance with reality.",
    },
    {
      icon: <DoneAllIcon color="success" />,
      label:
        "You won’t be able to make changes after submitting — please make sure you double-check everything.",
    },
  ];
  const afterListBodyTexts = ["Thank you!"];

  return (
    <InstructionsComponent
      instructionsTitle={instructionsTitle}
      bodyTexts={bodyTexts}
      listItems={listItems}
      afterListBodyTexts={afterListBodyTexts}
    />
  );
};

export default DocumentInstructions;
