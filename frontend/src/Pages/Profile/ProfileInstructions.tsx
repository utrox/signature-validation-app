import { Box, Typography } from "@mui/material";

const ProfileInstructions = () => {
  return (
    <Box sx={{ mb: 4, p: 2, backgroundColor: "#f5f5f5", borderRadius: 2 }}>
      <Typography variant="h6" gutterBottom>
        Your Profile
      </Typography>
      <Typography variant="body1">
        This page allows you to view your stored profile information. You cannot
        edit your profile information here, but you can do so in a physical
        location for security reasons.
      </Typography>
    </Box>
  );
};

export default ProfileInstructions;
