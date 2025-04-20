import React from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from "@mui/material";

type ListItem = {
  icon: React.ReactElement;
  label: string;
  instruction?: string;
};

interface InstructionsComponentProps {
  instructionsTitle: string;
  bodyTexts: string[];
  listItems: ListItem[];
  afterListBodyTexts?: string[];
}

const InstructionsComponent: React.FC<InstructionsComponentProps> = ({
  instructionsTitle,
  bodyTexts,
  listItems,
  afterListBodyTexts = [],
}) => {
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
        textAlign: "left"
      }}
    >
      <Typography variant="h6" gutterBottom>
        {instructionsTitle}
      </Typography>

      {bodyTexts.map((text, index) => (
        <Typography variant="body1" key={index}>
          {text}
        </Typography>
      ))}
      <List dense>
        {listItems.map((listItem) => (
          <ListItem
            sx={{ "&:hover": { backgroundColor: "rgba(0, 0, 0, 0.025)" } }}
            key={listItem.label}
          >
            <ListItemIcon>{listItem.icon}</ListItemIcon>
            <ListItemText
              primary={listItem.label}
              secondary={listItem.instruction}
            />
          </ListItem>
        ))}
      </List>

      {afterListBodyTexts.map((text, index) => (
        <Typography variant="body1" key={index}>
          {text}
        </Typography>
      ))}
    </Box>
  );
};

export default InstructionsComponent;
