import "./auth.css";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

import useAuth from "../../requests/useAuth";
import PageTitle from "../../components/Routing/PageTitle";
import axiosInstance from "../../requests/axios";

export const Register = () => {
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  // Redirect to home if user is already logged in
  const { user } = useAuth();
  if (user) {
    // Use window.location.href to reload, so we don't have
    // to manually refetch user data.
    window.location.href = "/";
  }

  const handleRegistration = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    await axiosInstance
      .post(`/auth/register/`, {
        email,
        username,
        password,
      })
      .then((_) => {
        toast.info("Registration successful. You can now log in.");
        navigate("/login");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div className="register">
      <PageTitle title="Register" />

      <div className="card">
        <div className="register-leftSide side">
          <h1>Register</h1>
          <form>
            <input
              type="text"
              placeholder="Username"
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              type="email"
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleRegistration}>
              {/* TODO: better loading component */}
              {loading ? "Loading..." : "Register"}
            </button>
          </form>
        </div>
        <div className="register-rightSide side">
          <h1>
            Welcome to <span id="logo">TODO name app</span>
          </h1>
          <p>
            Don't worry, you only need to provide a username, email and
            password. We'll take care of the rest, automatically generating
            dummy data so you can test this demo.
          </p>
          <p>Do you already have an account?</p>
          <div>
            <Link to="/login">
              <button>Log in</button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
