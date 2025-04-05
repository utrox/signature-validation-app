import { Route, Routes } from "react-router-dom";

// TODO: add confirm dialog import ConfirmationDialog from "./components/ConfirmDialog/index.tsx";
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

function App() {
  return (
    <>
      <PageTitle />
      {/*TODO: implement <ConfirmationDialog isOpen={showModal} {...modalProps} /> */}
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Main />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Routes protected with authentication + signatures recorded */}
        <Route element={<PrivateRoute />}>
          <Route path="/record-signatures" element={<RecordSignatures />} />

          {/* Routes that redirect user to record signatures, if they did not already do that. */}
          <Route element={<ValidSignaturesNeededRoute />}>
            <Route path="/demo" element={<DemoPage />} />
            <Route path="/documents" element={<Documents />} />
            <Route path="/documents/:id" element={<SingleDocument />} />
          </Route>
        </Route>
        <Route path="*" element={<h1>404 does not exist</h1>} />
      </Routes>
    </>
  );
}

export default App;
