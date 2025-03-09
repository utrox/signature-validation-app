import { Navigate, Outlet } from "react-router-dom";
import useAuth from "../../requests/useAuth";

export const ValidSignaturesNeededRoute = () => {
  const { user, isLoading } = useAuth();

  // Show a loading state while waiting for the auth status
  // TODO: better loading component
  if (isLoading) return <div>Loading...</div>;

  // Make sure the user has signatures recorded, before allowing them to use
  // the document page.
  return (user?.is_signatures_recorded) ? <Outlet /> : <Navigate to="/record-signatures" />;
};
