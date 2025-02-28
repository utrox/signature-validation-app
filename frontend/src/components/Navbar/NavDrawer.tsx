import {
  Box,
  Divider,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
} from "@mui/material";
import AppIcon from "../AppIcon";
import { useNavigate } from "react-router-dom";

const drawerWidth = 250;

interface NavDrawerProps {
  mobileOpen: boolean;
  handleDrawerToggle: () => void;
  pages: { name: string; url: string }[];
}

const NavDrawer: React.FC<NavDrawerProps> = ({
  mobileOpen,
  handleDrawerToggle,
  pages,
}) => {
  const navigate = useNavigate();
  return (
    <nav>
      <Drawer
        container={document.body}
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: "block", sm: "block", md: "none" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: drawerWidth,
          },
        }}
      >
        <Box onClick={handleDrawerToggle} sx={{ textAlign: "center" }}>
          <Typography variant="h6" sx={{ my: 2 }}>
            <AppIcon />
          </Typography>
          <Divider />
          <List>
            {pages.map((item) => (
              <ListItem key={item.name} disablePadding>
                <ListItemButton
                  sx={{ textAlign: "center" }}
                  onClick={() => navigate(item.url)}
                >
                  <ListItemText primary={item.name} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
    </nav>
  );
};

export default NavDrawer;
