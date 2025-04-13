import axiosInstance from "./axios";
import { useQuery } from "@tanstack/react-query";

const useAuth = () => {
  const fetchUserData = async () => {
    try {
      const { data } = await axiosInstance.get("/auth/me/");

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

  const logout = async () => {
    try {
      await axiosInstance.post("/auth/logout/");
      await refetch(); // clear user info
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return { user, isLoading, error, refetch, logout };
};

export default useAuth;
