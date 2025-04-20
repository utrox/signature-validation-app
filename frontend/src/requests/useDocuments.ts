import axiosInstance from "./axios";
import { useQuery } from "@tanstack/react-query";

export type ListDocumentData = {
  id: number;
  name: string;
};

const useDocuments = (id: string = "") => {
  const fetchDocuments = async (): Promise<ListDocumentData[]> => {
    try {
      const { data } = await axiosInstance.get<ListDocumentData[]>(
        `/api/documents/${id}`
      );
      return data;
    } catch (error) {
      return [];
    }
  };

  const {
    data: documents,
    isLoading,
    error,
  } = useQuery<ListDocumentData[]>({
    queryKey: ["documents"],
    queryFn: fetchDocuments,
    staleTime: 300000, // Cache for 5 minutes
    retry: 1,
  });

  return { documents, isLoading, error };
};

export default useDocuments;
