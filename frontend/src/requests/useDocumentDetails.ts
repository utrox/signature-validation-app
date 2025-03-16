import axiosInstance from "./axios";
import { useQuery } from "@tanstack/react-query";
import { DocumentData } from "../types/dynamic_form";

const useDocumentDetails = (id: string) => {
  const fetchDocumentDetails = async (): Promise<DocumentData | null> => {
    try {
      const { data } = await axiosInstance.get<DocumentData>(`/api/documents/${id}`);
      return data;
    } catch (error) {
      return null;
    }
  };

  const { data: document, isLoading, error } = useQuery<DocumentData | null>({
    queryKey: ["document"],
    queryFn: fetchDocumentDetails,
    staleTime: 300000, // Cache for 5 minutes
    retry: 1,
  });

  return { document, isLoading, error };
};

export default useDocumentDetails;
