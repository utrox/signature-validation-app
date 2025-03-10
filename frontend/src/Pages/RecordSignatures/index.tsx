import { Container, Paper, Box, Typography } from "@mui/material";
import { useState, useEffect } from "react";
import Page from "../../components/Page";
import SignatureCanvas, {
  SignatureData,
} from "../../components/SignatureCanvas";
import useRegisterSignatures from "../../requests/useRegisterSignatures";
import useAuth from "../../requests/useAuth";
import RecordSignatureInstructions from "./Instructions";

const PHYSICAL_SIGNATURE_PLACE = import.meta.env.VITE_PHYSICAL_PLACE === "true";
const REGISTRATION_SIGNATURES_NEEDED = import.meta.env
  .VITE_REGISTRATION_SIGNATURES_NEEDED;

const RecordSignatures = () => {
  const [signatures, setSignatures] = useState<SignatureData[]>([]);
  const [showSignatures, setShowSignatures] = useState(true);
  const { mutate: queryRegisterSignatures } = useRegisterSignatures();

  const { user } = useAuth();

  // Don't let them resize the window under 700px and still use the signature function.
  const handleResize = () => {
    setShowSignatures(window.innerWidth >= 700);
  };

  useEffect(() => {
    window.addEventListener("resize", handleResize);
    handleResize();
  });

  useEffect(() => {
    if (signatures.length == REGISTRATION_SIGNATURES_NEEDED)
      queryRegisterSignatures(signatures);
    console.log("We da best");
  }, [signatures]);

  const addSignature = (signatureData: SignatureData) =>
    setSignatures([...signatures, signatureData]);

  const renderContent = () => {
    if (!PHYSICAL_SIGNATURE_PLACE || !showSignatures) {
      return (
        <Typography variant="h6" color="error" align="center">
          Please go to a terminal at a physical location to record your
          signatures.
        </Typography>
      );
    }
    if (user.is_signatures_recorded) {
      return (
        <Typography variant="h6" color="success" align="center">
          You've already recorded your signatures.
        </Typography>
      );
    }
    return (
      <>
        <Typography>
          You've submitted {signatures.length} signature(s) out of{" "}
          {REGISTRATION_SIGNATURES_NEEDED}.
        </Typography>
        {signatures.length < REGISTRATION_SIGNATURES_NEEDED ? (
          <SignatureCanvas onSave={addSignature} />
        ) : (
          <Typography variant="h6" color="success" align="center">
            You're done, bozo!
          </Typography>
        )}
      </>
    );
  };
  return (
    <Page title="Register signature">
      <Container component="main">
        <Paper
          sx={{
            padding: 3,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <RecordSignatureInstructions />
          <Box sx={{ width: "100%", marginBottom: 2 }}>{renderContent()}</Box>
        </Paper>
      </Container>
    </Page>
  );
};

export default RecordSignatures;
