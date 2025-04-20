import { Typography } from "@mui/material";

const WelcomeText = () => {
  return (
    <>
      <Typography variant="h4" gutterBottom>
        Welcome to{" "}
        <span style={{ color: "#1976d2", fontWeight: 700 }}>
          {import.meta.env.VITE_APP_NAME}
        </span>
      </Typography>
      <Typography variant="body1">
        Don't worry, you only need to provide a username, email, and password.
        We'll take care of the rest, automatically generating dummy data so you
        can test this demo.
      </Typography>
    </>
  );
};

export default WelcomeText;
