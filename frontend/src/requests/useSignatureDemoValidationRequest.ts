import { toast } from "react-toastify";
import axiosInstance from "./axios";
import { useMutation } from "@tanstack/react-query";
import { SignatureData } from "../components/SignatureCanvas";

const useSignatureDemoValidationRequest = () => {
  const demoValidationRequest = async (signature: SignatureData) => {
    const { data } = await axiosInstance.post("/api/signatures/demo-verify/", signature);
    return data;
  };

  const mutation = useMutation({
    mutationFn: demoValidationRequest,
    onSuccess: () => {
      toast.info("Your signature request has been processed!");
    },
  });

  return mutation;
};

export default useSignatureDemoValidationRequest;
