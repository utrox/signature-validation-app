import { toast } from "react-toastify";
import axiosInstance from "./axios";
import { useMutation } from "@tanstack/react-query";
import { SignatureData } from "../components/SignatureCanvas";

const useRegisterSignatures = () => {
  const registerSignature = async (signatures: SignatureData[]) => {
    const { data } = await axiosInstance.post("/api/signatures/", signatures);
    return data;
  };

  const mutation = useMutation({
    mutationFn: registerSignature,
    onSuccess: () => {
      toast.info("Signatures successfully recorded!");
    },
  });

  return mutation;
};

export default useRegisterSignatures;
