import axios from "axios";
import { toast } from "react-toastify";
import { getCSRFToken } from "./csrf";

// Create Axios instance
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
  timeout: 5000,
  withCredentials: true,
});

// Add the CSRF token to the headers for every request
axiosInstance.interceptors.request.use(
  (config) => {
    const csrfToken = getCSRFToken(); // Call the method to get the CSRF token

    // Add CSRF token to the headers
    if (csrfToken) {
      config.headers["X-CSRFToken"] = csrfToken;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add global error-handling interceptor for every response
axiosInstance.interceptors.response.use(
  (response) => {
    // Return the response if everything is alright
    return response;
  },
  (error) => {
    // Catch any error and show a Toast
    console.error(error);

    if (error?.response?.data?.errors) {
      error.response.data.errors.forEach((err: { message: string }) => {
        toast.error(err.message);
      });
    } else {
      toast.error("There was an unhandled error. Please try again later.");
    }

    // Reject the promise to continue error flow
    return Promise.reject(error);
  }
);

export default axiosInstance;
