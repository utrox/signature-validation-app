import { Card, CardContent, Typography, Box } from "@mui/material";

interface UserProfileProps {
  profile: {
    first_name: string;
    last_name: string;
    address: string;
    phone: string;
    date_of_birth: string;
    bank_account_number: string;
  } | null;
}

const UserProfile: React.FC<UserProfileProps> = ({ profile }) => {
  if (!profile) {
    return (
      <Typography variant="h6" align="center" mt={10}>
        No profile data available.
      </Typography>
    );
  }

  return (
    <Box maxWidth="600px" mx="auto" mt={5}>
      <Card variant="outlined" sx={{ borderRadius: 3, boxShadow: 3 }}>
        <CardContent>
          <Typography variant="body1">
            <strong>First Name:</strong> {profile.first_name}
          </Typography>
          <Typography variant="body1">
            <strong>Last Name:</strong> {profile.last_name}
          </Typography>
          <Typography variant="body1">
            <strong>Address:</strong> {profile.address}
          </Typography>
          <Typography variant="body1">
            <strong>Phone:</strong> {profile.phone}
          </Typography>
          <Typography variant="body1">
            <strong>Date of Birth:</strong> {profile.date_of_birth}
          </Typography>
          <Typography variant="body1">
            <strong>Bank Account Number:</strong> {profile.bank_account_number}
          </Typography>
          <Typography
            variant="caption"
            display="block"
            mt={3}
            color="text.secondary"
          >
            To change your profile information, please visit your nearest bank branch.
          </Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default UserProfile;
