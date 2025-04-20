import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import {
  TextField,
  Button,
  Box,
  Paper,
  Typography,
  CircularProgress,
  Container,
} from "@mui/material";

import useAuth from "../../requests/useAuth";
import axiosInstance from "../../requests/axios";
import Page from "../../components/Page";
import WelcomeText from "./WelcomeText";

export const Register = () => {
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  // Redirect to home if user is already logged in
  const { user } = useAuth();
  if (user) {
    window.location.href = "/";
  }

  const handleRegistration = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axiosInstance.post(`/auth/register/`, {
        username,
        email,
        password,
      });
      toast.info("Registration successful. You can now log in.");
      navigate("/login");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Page title="Register">
      <Container maxWidth="md">
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: "flex",
            flexDirection: { xs: "column-reverse", sm: "row" },
            gap: 4,
          }}
        >
          <Box flex={1}>
            <Typography variant="h5" gutterBottom>
              Register
            </Typography>
            <Box
              component="form"
              onSubmit={handleRegistration}
              display="flex"
              flexDirection="column"
              gap={2}
            >
              <TextField
                label="Username"
                variant="outlined"
                fullWidth
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              <TextField
                label="Email"
                variant="outlined"
                type="email"
                fullWidth
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <TextField
                label="Password"
                variant="outlined"
                type="password"
                fullWidth
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button type="submit" variant="contained" disabled={loading}>
                {loading ? <CircularProgress size={24} /> : "Register"}
              </Button>
            </Box>
          </Box>
          <Box
            flex={1}
            display="flex"
            flexDirection="column"
            justifyContent="center"
          >
            <WelcomeText />
            <Typography variant="body2">Already have an account?</Typography>
            <Button
              variant="outlined"
              component={Link}
              to="/login"
              sx={{ mt: 2, width: "fit-content" }}
            >
              Login
            </Button>
          </Box>
        </Paper>
      </Container>
    </Page>
  );
};

export default Register;
