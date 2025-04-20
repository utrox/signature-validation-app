import { useState } from "react";
import { Link } from "react-router-dom";
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

export const Login = () => {
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { user } = useAuth();

  if (user) {
    window.location.href = "/";
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axiosInstance.post(`/auth/login/`, {
        username,
        password,
      });
      toast.info("Login successful.");
      window.location.href = "/";
    } finally {
      setLoading(false);
    }
  };

  return (
    <Page title="Login">
      <Container maxWidth="md">
        <Paper
          elevation={3}
          sx={{
            p: 4,
            display: "flex",
            flexDirection: {
              xs: "column",
              sm: "row",
            },
            gap: 4,
          }}
        >
          <Box
            flex={1}
            display="flex"
            flexDirection="column"
            justifyContent="center"
          >
            <WelcomeText />
            <Typography variant="body2">
              If you don't have an account, create one!
            </Typography>
            <Button
              variant="outlined"
              component={Link}
              to="/register"
              sx={{ mt: 2, width: "fit-content" }}
            >
              Register
            </Button>
          </Box>
          <Box flex={1}>
            <Typography variant="h5" gutterBottom>
              Login
            </Typography>
            <Box
              component="form"
              onSubmit={handleLogin}
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
                label="Password"
                variant="outlined"
                type="password"
                fullWidth
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Button type="submit" variant="contained" disabled={loading}>
                {loading ? <CircularProgress size={24} /> : "Login"}
              </Button>
            </Box>
          </Box>
        </Paper>
      </Container>
    </Page>
  );
};

export default Login;
