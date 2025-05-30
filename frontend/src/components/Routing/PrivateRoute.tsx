import { Navigate, Outlet } from "react-router-dom";
import useAuth from "../../requests/useAuth";

export const PrivateRoute = () => {
  const { user, isLoading } = useAuth();

  // Show a loading state while waiting for the auth status
  // TODO: better loading component
  if (isLoading) return <div>Loading...</div>;

  // If user is not authenticated, redirect to login
  return user ? <Outlet /> : <Navigate to="/login" />;
};
