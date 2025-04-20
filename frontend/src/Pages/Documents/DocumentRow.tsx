import { Link } from "react-router-dom";
import { IconButton, ListItem, ListItemText, Tooltip } from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import { ListDocumentData } from "../../requests/useDocuments";

interface DocumentRowProps {
  document: ListDocumentData;
  key: number;
}

const DocumentRow: React.FC<DocumentRowProps> = ({document, key}) => {
  return (
    <Link to={`/documents/${document.id}`}>
      <ListItem key={key} className="doc-list-item">
        <ListItemText primary={document.name} />
        <Tooltip title="View">
          <IconButton>
            <VisibilityIcon color="primary" />
          </IconButton>
        </Tooltip>
      </ListItem>
    </Link>
  );
};

export default DocumentRow;
