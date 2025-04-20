import { useNavigate } from "react-router-dom";
import { Box, Typography, Container, Button } from "@mui/material";

import Page from "../../components/Page";
import useAuth from "../../requests/useAuth";
import MainInstructions from "./MainInstructions";

const UserGuide = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const tryDemoOnClick = user
    ? () => navigate("/documents")
    : () => navigate("/login");

  return (
    <Page>
      <Container maxWidth="md" sx={{ textAlign: "center", mt: 4 }}>
        <Typography variant="h3" gutterBottom>
          Welcome to the{" "}
          <span style={{ color: "#1976d2", fontWeight: 700 }}>DAMN</span>{" "}
          Signature Validation System
        </Typography>

        <Typography variant="h6">
          {import.meta.env.VITE_APP_NAME} - {import.meta.env.VITE_APP_LONG_NAME}{" "}
          is a secure and efficient way to handle electronic documents with
          signature verification.
        </Typography>
        <MainInstructions />
        <Box sx={{ textAlign: "center" }}>
          <Button
            onClick={tryDemoOnClick}
            variant="contained"
            color="primary"
            size="large"
          >
            {user ? "Try the Demo" : "Log in"}
          </Button>
        </Box>
      </Container>
    </Page>
  );
};

export default UserGuide;
