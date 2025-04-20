import axiosInstance from "./axios";
import { useQuery } from "@tanstack/react-query";

const useAuth = () => {
  const fetchUserData = async () => {
    try {
      const { data } = await axiosInstance.get("/user/me/");

      return data; // If user is logged in, this will return user data
    } catch (error) {
      return null; // If the user isn't logged in, return null
    }
  };

  const fetchUserProfileData = async () => {
    try {
      const { data } = await axiosInstance.get("/user/profile/");
      return data; // If user is logged in, this will return user data
    } catch (error) {
      return null; // If the user isn't logged in, return null
    }
  };

  const {
    data: user,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ["me"],
    queryFn: fetchUserData,
    staleTime: 300000, // Cache for 5 minutes
    retry: 1, // Only retry once on failure
  });

  const {
    data: profileData,
    isLoading: isLoadingProfile,
    error: errorProfile,
  } = useQuery({
    queryKey: ["profile"],
    queryFn: fetchUserProfileData,
    staleTime: 300000, // Cache for 5 minutes
    retry: 1, // Only retry once on failure
  });

  const logout = async () => {
    try {
      await axiosInstance.post("/auth/logout/");
      window.location.href = "/login"; // Redirect to login page after logout
      await refetch(); // clear user info
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return {
    user,
    isLoading,
    error,
    userProfile: {
      profileData,
      isLoadingProfile,
      errorProfile,
    },
    refetch,
    logout,
  };
};

export default useAuth;
