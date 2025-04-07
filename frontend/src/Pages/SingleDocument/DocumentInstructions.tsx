import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

import ElectricBoltIcon from '@mui/icons-material/ElectricBolt';
import Lock from "@mui/icons-material/Lock";
import GradingIcon from '@mui/icons-material/Grading';
import DoneAllIcon from '@mui/icons-material/DoneAll';

const DocumentInstructions = () => {
  return (
    <Box sx={{ mb: 4, p: 2, backgroundColor: "#f5f5f5", borderRadius: 2 }}>
      <Typography variant="h6" gutterBottom>
        Before you begin...
      </Typography>

      <Typography variant="body1">
        Please complete the following information related to this document.
      </Typography>

      <List dense>
        <ListItem>
          <ListItemIcon>
            <ElectricBoltIcon style={{color: "orange"}} />
          </ListItemIcon>
          <ListItemText primary="The data you enter here will help us generate your document with lightning speed." />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <Lock color="primary" />
          </ListItemIcon>
          <ListItemText primary="All information will be securely stored." />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <GradingIcon color="secondary" />
          </ListItemIcon>
          <ListItemText primary="Entries will be reviewed by a clerk prior to final approval, so please make sure they are in accordance with reality." />
        </ListItem>
        <ListItem>
          <ListItemIcon>
            <DoneAllIcon color="success" />
          </ListItemIcon>
          <ListItemText primary="You won’t be able to make changes after submitting — please make sure you double-check everything." />
        </ListItem>
      </List>

      <Typography variant="body2" sx={{ mt: 2 }}>
        Thank you!
      </Typography>
    </Box>
  );
};

export default DocumentInstructions;
