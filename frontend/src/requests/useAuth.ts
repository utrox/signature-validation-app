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

  const { data: user, isLoading, error } = useQuery({
    queryKey: ["me"],
    queryFn: fetchUserData,
    staleTime: 300000, // Cache for 5 minutes
    retry: 1,  // Only retry once on failure
  });


  return { user, isLoading, error };
};

export default useAuth;