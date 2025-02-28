import { Toolbar, Typography } from "@mui/material";

import AppIcon from "../AppIcon";

const NavIcon = () => {
  return (
    <>
      {/* TODO: navigation */}
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
        component="a"
        sx={{
          mr: 2,
          display: { xs: "none", md: "flex" },
          fontFamily: "monospace",
          fontWeight: 700,
          letterSpacing: ".3rem",
          color: "inherit",
          textDecoration: "none",
        }}
      >
        TODO appname
      </Typography>
    </>
  );
};

export default NavIcon;
