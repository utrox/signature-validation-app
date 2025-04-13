import { toast } from "react-toastify";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axiosInstance from "./axios";

const useDeleteWorkflow = () => {
  const queryClient = useQueryClient();

  const deleteWorkflow = async (id: string) => {
    await axiosInstance.delete(`/api/workflows/`, {
      data: { id },
    });
  };

  return useMutation({
    mutationFn: deleteWorkflow,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["workflows"] });
      toast.success("Workflow deleted successfully");
    },
  });
};

export default useDeleteWorkflow;
// TODO: organize requests folder into subfolders.
// For example requests/workflows/useDeleteWorkflow.ts
// requests/workflows/useWorkflows.ts
