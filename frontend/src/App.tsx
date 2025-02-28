import { Route, Routes } from "react-router-dom";

// import ConfirmationDialog from "./components/ConfirmDialog/index.tsx";
import { Login } from "./Pages/authentication/Login.tsx";
import { Register } from "./Pages/authentication/Register.tsx";
import { PrivateRoute } from "./components/Routing/PrivateRoute.tsx";
import PageTitle from "./components/Routing/PageTitle.tsx";

function App() {
  return (
    <>
      <PageTitle />
      {/*TODO: implement <ConfirmationDialog isOpen={showModal} {...modalProps} /> */}
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Routes protected with authentication */}
        <Route element={<PrivateRoute />}>
          <Route path="*" element={<h1>404 does not exist</h1>} />
        </Route>
      </Routes>
    </>
  );
}

export default App;
