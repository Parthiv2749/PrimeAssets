// ProtectedRoute.js
import React, { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
// import AuthContext from "./AuthContext";
import AuthContext from "../ApiService/api.js";

const ProtectedRoute = () => {
  const { user } = useContext(AuthContext);

  // If not authenticated, redirect to the login page
  console.log(user);
  if (!user) {
    return <Navigate to="/" replace />;
  }

  // If authenticated, render the child routes
  return <Outlet />;

};

export default ProtectedRoute;
