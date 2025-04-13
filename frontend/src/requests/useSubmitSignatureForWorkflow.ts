import { toast } from "react-toastify";
import axiosInstance from "./axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { SignatureData } from "../components/SignatureCanvas";

interface SubmitSignatureProps {
  workflowId: string;
  signature: SignatureData;
}

const useSubmitSignatureForWorkflow = () => {
  const queryClient = useQueryClient();
  const submitSignature = async ({
    workflowId,
    signature,
  }: SubmitSignatureProps) => {
    const { data } = await axiosInstance.patch("/api/workflows/", {
      id: workflowId,
      signature_data: signature,
    });
    return data;
  };

  const mutation = useMutation({
    mutationFn: submitSignature,
    onSuccess: () => {
      toast.success("Document signed successfully!");
    },
    onSettled: () => {
      // Invalidate 'workflows' query to refetch the data
      queryClient.invalidateQueries({ queryKey: ["workflows"] });
    },
  });

  return mutation;
};

export default useSubmitSignatureForWorkflow;
