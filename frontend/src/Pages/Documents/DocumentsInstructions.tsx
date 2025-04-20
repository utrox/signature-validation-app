import FolderIcon from "@mui/icons-material/Folder";
import SearchIcon from "@mui/icons-material/Search";
import DescriptionIcon from "@mui/icons-material/Description";
import HowToRegIcon from "@mui/icons-material/HowToReg";
import InstructionsComponent from "../../components/Instructions";

const AllDocumentsInstructions = () => {
  const instructionsTitle = "How to Manage Your Documents";
  const bodyTexts = ["Follow these steps to view and manage your documents."];

  const listItems = [
    {
      icon: <FolderIcon style={{ color: "orange" }} />,
      label: "Browse through the available documents in the list below.",
    },
    {
      icon: <SearchIcon color="primary" />,
      label: "Use the search bar to quickly find a specific document.",
    },
    {
      icon: <DescriptionIcon color="secondary" />,
      label:
        "Click on a document title to view, fill out it's details, and submit it.",
    },
    {
      icon: <HowToRegIcon color="success" />,
      label:
        "After that, all you need to do is wait for us to review and accept your document!",
    },
  ];

  const afterListBodyTexts = [
    "If you have any questions or need assistance, please contact our support team.",
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

export default AllDocumentsInstructions;
