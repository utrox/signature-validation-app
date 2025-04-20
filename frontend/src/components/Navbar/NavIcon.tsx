import { Typography } from "@mui/material";

import AppIcon from "../AppIcon";
import { Link } from "react-router-dom";

const NavIcon = () => {
  return (
    <Link
      to={"/"}
      style={{
        display: "flex",
        alignItems: "center",
        textDecoration: "none",
      }}
    >
      <AppIcon
        sx={{
          display: { xs: "none", md: "flex" },
          mr: 1,
          color: "white",
        }}
      />
      <Typography
        variant="h6"
        noWrap
        sx={{
          mr: 2,
          display: { xs: "none", md: "flex" },
          fontFamily: "monospace",
          fontWeight: 700,
          letterSpacing: ".3rem",
          color: "white",
          textDecoration: "none",
        }}
      >
        {import.meta.env.VITE_APP_NAME}
      </Typography>
    </Link>
  );
};

export default NavIcon;
