import {
  CheckCircle,
  Description,
  Email,
  HowToReg,
  Person,
  Security,
  Verified,
} from "@mui/icons-material";
import InstructionsComponent from "../../components/Instructions";

const MainInstructions = () => {
  const instructionsTitle = "How It Works";
  const bodyTexts = [
    "The DAMN - Digital Authorization & Motion-based Notarization is a secure and efficient way to handle electronic documents with signature verification.\
    This system allows you to submit documents electronically, have them reviewed by a bank clerk, and sign them securely at a terminal.",
  ];
  const listItems = [
    {
      icon: <Person style={{ color: "blue" }} />,
      label: "Step 1: Fill out the form online",
      instruction:
        "Log in to your account, fill out the required information, and submit the form electronically.",
    },
    {
      icon: <Verified color="success" />,
      label: "Step 2: Clerk reviews and approves your document",
      instruction:
        "A bank clerk will review your form and either approve or reject it based on the filled-out data.",
    },
    {
      icon: <Email color="primary" />,
      label: "Step 3: Notification email",
      instruction:
        "If your form is approved, you'll receive an email with a unique document ID. If rejected, you'll get an explanation of why.",
    },
    {
      icon: <Security color="warning" />,
      label: "Step 4: Visit the terminal",
      instruction:
        "Go to the physical location and log in using your username, password, and document ID. SMS 2FA will be added for extra security in the real-world scenario.",
    },
    {
      icon: <Description color="secondary" />,
      label: "Step 5: Review your document",
      instruction:
        "Review the submitted information on the terminal. Double-check your document before proceeding to the signing.",
    },
    {
      icon: <HowToReg color="success" />,
      label: "Step 6: Sign the document",
      instruction:
        "Once you accept the document, sign it on the terminal. Your signature will be validated against previous ones to minimize fraud.",
    },
    {
      icon: <CheckCircle color="primary" />,
      label: "Step 7: All done!",
      instruction:
        "After signing, the process is complete! No more waiting in line at the clerk's desk — everything is handled electronically.",
    },
  ];

  const afterListBodyTexts = [
    "Thank you for using our system! If you have any questions or need assistance, please contact our support team.",
  ];
  return (
    <InstructionsComponent
      instructionsTitle={instructionsTitle}
      bodyTexts={bodyTexts}
      listItems={listItems}
      afterListBodyTexts={afterListBodyTexts}
    />
  );
};

export default MainInstructions;
