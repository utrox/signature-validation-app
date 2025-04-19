import useAuth from "../../requests/useAuth";
import Page from "../../components/Page";
import ProfileInstructions from "./ProfileInstructions";
import UserProfile from "./UserProfile";
import { Container } from "@mui/material";

const ProfilePage = () => {
  const { userProfile } = useAuth();
  return (
    <Page title="Profile">
        <Container maxWidth="sm">
        <ProfileInstructions/>
        <UserProfile profile={userProfile.profileData || null} />
        </Container>
    </Page>
  );
};

export default ProfilePage;
