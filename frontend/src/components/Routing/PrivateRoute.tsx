// import { useAuth } from "../hooks/useAuth";
import { Navigate, Outlet } from "react-router-dom";

export const PrivateRoute = () => {
  //TODO: reimplement without GraphQL: const { user, loading } = useAuth();
  const loading = false;
  const user = true;

  // Show a loading state while waiting for the auth status
  // TODO: better loading component
  if (loading) return <div>Loading...</div>;

  // If user is not authenticated, redirect to login
  return user ? <Outlet /> : <Navigate to="/login" />;
};
