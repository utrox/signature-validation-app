import { toast } from "react-toastify";
import axiosInstance from "./axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { FormState } from "../types/dynamic_form";

interface CreateSignatureWorkflowData {
  document_id: string;
  form_data: FormState;
}

const useSubmitSignatureWorkflow = () => {
  const queryClient = useQueryClient();

  const submitSignatureWorkflow = async (
    workflowData: CreateSignatureWorkflowData
  ) => {
    const { data } = await axiosInstance.post("/api/workflows/", workflowData);
    return data;
  };

  const mutation = useMutation({
    mutationFn: submitSignatureWorkflow,
    onSuccess: () => {
      toast.success("Document successfully submitted for review by clerk!");
      // Refetch workflows
      queryClient.invalidateQueries({ queryKey: ["workflows"] });
    },
  });

  return mutation;
};

export default useSubmitSignatureWorkflow;
