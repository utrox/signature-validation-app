import "./auth.css";
import { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

import useAuth from "../../requests/useAuth";
import PageTitle from "../../components/Routing/PageTitle";
import axiosInstance from "../../requests/axios";

export const Login = () => {
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { user } = useAuth();

  // Redirect to home if user is already logged in
  // const { user } = useAuth();
  if (user) {
    // Use window.location.href to redirect,
    // so it reloads the whole app and fetches the user data again.
    window.location.href = "/";
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    await axiosInstance
      .post(`/auth/login/`, {
        username,
        password,
      })
      .then(() => {
        toast.info("Login successful.");
        window.location.href = "/";
      })
      .finally(() => setLoading(false));
  };

  return (
    <div className="login">
      <PageTitle title="Login" />
      <div className="card">
        <div className="login-leftSide side">
          <h1>
            Welcome to <span id="logo">TODO name app</span>
          </h1>
          <p>
            Don't worry, you only need to provide a username, email and
            password. We'll take care of the rest, automatically generating
            dummy data so you can test this demo.
          </p>
          <p>If you don't have an account, create one!</p>
          <div>
            <Link to="/register">
              <button>Register</button>
            </Link>
          </div>
        </div>
        <div className="login-rightSide side">
          <h1>Login</h1>
          <form>
            <input
              type="text"
              placeholder="Username"
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />
            {/* TODO: better loading component */}
            <button onClick={handleLogin}>
              {loading ? "Loading..." : "Login"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
