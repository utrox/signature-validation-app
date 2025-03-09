import axiosInstance from "./axios";
import { useQuery } from "@tanstack/react-query";

type DocumentData = {
    id: number,
    name: string
}

const useDocuments = (id: string = "") => {
  const fetchDocuments = async (): Promise<DocumentData[]> => {
    try {
      const { data } = await axiosInstance.get<DocumentData[]>(`/api/documents/${id}`);
      return data;
    } catch (error) {
      return [];
    }
  };

  const { data: documents, isLoading, error } = useQuery<DocumentData[]>({
    queryKey: ["documents"],
    queryFn: fetchDocuments,
    staleTime: 300000, // Cache for 5 minutes
    retry: 1,
  });

  return { documents, isLoading, error };
};

export default useDocuments;
