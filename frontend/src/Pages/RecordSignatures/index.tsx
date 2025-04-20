import { useState, useEffect } from "react";
import { Container, Paper, Box, Typography } from "@mui/material";

import Page from "../../components/Page";
import SignatureCanvas, {
  SignatureData,
} from "../../components/SignatureCanvas";
import useRegisterSignatures from "../../requests/useRegisterSignatures";
import useAuth from "../../requests/useAuth";
import RecordSignatureInstructions from "./Instructions";

const REGISTRATION_SIGNATURES_NEEDED = import.meta.env
  .VITE_REGISTRATION_SIGNATURES_NEEDED;

const RecordSignatures = () => {
  const [signatures, setSignatures] = useState<SignatureData[]>([]);
  const {
    mutate: queryRegisterSignatures,
    isSuccess,
    isPending,
    isError,
  } = useRegisterSignatures();

  const { user, refetch } = useAuth();

  useEffect(() => {
    if (signatures.length == REGISTRATION_SIGNATURES_NEEDED)
      queryRegisterSignatures(signatures);
  }, [signatures]);

  useEffect(() => {
    if (isSuccess) refetch();
  }, [isSuccess]);

  const addSignature = (signatureData: SignatureData) =>
    setSignatures([...signatures, signatureData]);

  const renderContent = () => {
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
        {isPending && (
          <Typography>
            Loading... Please wait, this might take up to a couple a minutes.
          </Typography>
        )}
        {}
        {signatures.length < REGISTRATION_SIGNATURES_NEEDED ? (
          <SignatureCanvas onSave={addSignature} isLoading={isPending} />
        ) : (
          isSuccess && (
            <Typography variant="h6" color="success" align="center">
              You're done, bozo!
            </Typography>
          )
        )}
        {isError && (
          <Typography variant="h6" color="error" align="center">
            There was an error while saving your signatures. Please try again.
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
