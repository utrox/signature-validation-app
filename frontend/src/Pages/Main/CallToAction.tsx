import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Button,
  Container,
  Box,
} from "@mui/material";

const UserGuide = () => {
  return (
    <Container maxWidth="md">
      <Box sx={{ textAlign: "center", marginBottom: 4 }}>
        <Typography variant="h3" gutterBottom>
          Welcome to Our Signature Validation System
        </Typography>
        <Typography variant="h6">
          A secure and efficient way to handle electronic documents with
          signature verification.
        </Typography>
      </Box>

      <Typography variant="h5" sx={{ marginBottom: 2 }}>
        How It Works:
      </Typography>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 1 }}>
            Step 1: Fill out the form online
          </Typography>
          <Typography variant="body1">
            Log in to your account, fill out the required information, and
            submit the form electronically.
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 1 }}>
            Step 2: Clerk reviews and approves/rejects
          </Typography>
          <Typography variant="body1">
            A bank clerk will review your form and either approve or reject it
            based on the filled-out data.
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 1 }}>
            Step 3: Notification email
          </Typography>
          <Typography variant="body1">
            If your form is approved, you'll receive a success message with a
            unique document ID. If rejected, the email will explain why.
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 1 }}>
            Step 4: Visit the terminal
          </Typography>
          <Typography variant="body1">
            Go to the physical location and log in using your username,
            password, and document ID. (Later, we'll include 2FA for added
            security!)
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 1 }}>
            Step 5: Review your document
          </Typography>
          <Typography variant="body1">
            Review your submitted information on the terminal. You can
            double-check your document before proceeding to the signing.
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 1 }}>
            Step 6: Sign the document
          </Typography>
          <Typography variant="body1">
            Once you accept the document, sign it on the terminal. Your
            signatire will be validated against your previous signatures, to
            minimize the chance of fraud happening.
          </Typography>
        </CardContent>
      </Card>

      <Card sx={{ marginBottom: 4 }}>
        <CardContent>
          <Typography variant="h6" sx={{ marginBottom: 1 }}>
            Step 7: All done!
          </Typography>
          <Typography variant="body1">
            After signing, the process is complete! No more waiting in line at
            the clerk's desk — everything is handled electronically.
          </Typography>
        </CardContent>
      </Card>

      <Box sx={{ textAlign: "center" }}>
        <Button variant="contained" color="primary" size="large">
          Try the Demo
        </Button>
      </Box>
    </Container>
  );
};

export default UserGuide;
