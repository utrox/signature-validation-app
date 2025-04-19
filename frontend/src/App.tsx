import { Route, Routes } from "react-router-dom";

import Main from "./Pages/Main";
import { Login } from "./Pages/authentication/Login.tsx";
import { Register } from "./Pages/authentication/Register.tsx";
import { PrivateRoute } from "./components/Routing/PrivateRoute.tsx";
import { ValidSignaturesNeededRoute } from "./components/Routing/ValidSignaturesNeededRoute.tsx";
import PageTitle from "./components/Routing/PageTitle.tsx";
import Documents from "./Pages/Documents/index.tsx";
import SingleDocument from "./Pages/SingleDocument/index.tsx";
import RecordSignatures from "./Pages/RecordSignatures/index.tsx";
import DemoPage from "./Pages/Demo/index.tsx";
import WorkflowsPage from "./Pages/Workflows/index.tsx";
import ProfilePage from "./Pages/Profile/index.tsx";

function App() {
  return (
    <>
      <PageTitle />
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Main />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Routes protected with authentication only, no recorded signatures. */}
        <Route element={<PrivateRoute />}>
          <Route path="/record-signatures" element={<RecordSignatures />} />
          <Route path="/profile" element={<ProfilePage />} />

          {/* Routes that redirect user to record signatures, if they did not already do that. */}
          <Route element={<ValidSignaturesNeededRoute />}>
            <Route path="/demo" element={<DemoPage />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/documents/:id" element={<SingleDocument />} />
            <Route path="/workflows" element={<WorkflowsPage />} />
          </Route>
        </Route>
        <Route path="*" element={<h1>404 does not exist</h1>} />
      </Routes>
    </>
  );
}

export default App;
