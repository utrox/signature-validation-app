import axiosInstance from "./axios";
import { useQuery } from "@tanstack/react-query";
import { WorkflowData } from "../Pages/Workflows/types";

const useWorkflows = () => {
  const fetchWorkflows = async (): Promise<WorkflowData[]> => {
    try {
      const { data } = await axiosInstance.get<WorkflowData[]>(
        `/api/workflows/`
      );
      return data;
    } catch (error) {
      return [];
    }
  };

  const {
    data: workflows,
    isLoading,
    error,
  } = useQuery<WorkflowData[]>({
    queryKey: ["workflows"],
    queryFn: fetchWorkflows,
    staleTime: 300000, // Cache for 5 minutes
    retry: 1,
    refetchOnMount: true,
  });

  return { workflows, isLoading, error };
};

export default useWorkflows;
