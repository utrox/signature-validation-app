import { CheckCircle, Clear, DrawOutlined, Biotech } from "@mui/icons-material";
import InstructionsComponent from "../../components/Instructions";

const DemoPageInstuctions = () => {
  const instructionsTitle = "How to use the Signature Validation DEMO page?";
  const bodyTexts = [
    "Do you only care about the cool part? The signature validation? Then this is the page for you!",
    "Follow these steps to make sure you can try out our signature validation system!",
  ];
  const listItems = [
    {
      icon: <DrawOutlined style={{ color: "blue" }} />,
      label: "Draw your signature",
      instruction:
        "In the empty box below, draw your signature using your stylus. Make sure you are being dynamic but accurate.",
    },
    {
      icon: <Biotech color="secondary" />,
      label: "Validation",
      instruction:
        "Once you've drawn your signature, our system will validate it against your saved signatures. You'll know almost immediately if it's accepted or rejected.",
    },
    {
      icon: <Clear color="error" />,
      label: "Clear the board (if needed)",
      instruction:
        "If you make a mistake or want to try again, simply click the 'Clear Board' button to reset the board and start over.",
    },
    {
      icon: <CheckCircle color="success" />,
      label: "Signature Accepted or Rejected",
      instruction:
        "If the system accepts your signature, you're good to go! If it's rejected, try again and ensure your signature matches your previously saved ones.",
    },
  ];

  return (
    <InstructionsComponent
      instructionsTitle={instructionsTitle}
      bodyTexts={bodyTexts}
      listItems={listItems}
    />
  );
};

export default DemoPageInstuctions;
