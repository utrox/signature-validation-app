import { Container, Typography } from "@mui/material";

import Page from "../../components/Page";
import SignatureCanvas, {
  SignatureData,
} from "../../components/SignatureCanvas";
import useSignatureDemoValidationRequest from "../../requests/useSignatureDemoValidationRequest";
import { isAxiosError } from "axios"; // make sure you import this
import DemoPageInstuctions from "./DemoPageInstuctions";

const DemoPage = () => {
  const {
    isPending,
    isSuccess,
    error,
    mutate: querySignatureDemoValidationRequest,
  } = useSignatureDemoValidationRequest();
  console.error("ERROR: ", error);

  const addSignature = (signatureData: SignatureData) => {
    querySignatureDemoValidationRequest(signatureData);
  };

  return (
    <Page title="Demo">
      <Container maxWidth="md">
        <Typography variant="h4" gutterBottom>
          Demo Page
        </Typography>
        <DemoPageInstuctions />
        <SignatureCanvas onSave={addSignature} isLoading={isPending} />

        {isSuccess && (
          <Typography variant="h6" color="success" align="center">
            Congratulations! Your signature is either valid, or you're good at
            forging signatures.
          </Typography>
        )}

        {error && (
          <Typography variant="h6" color="error" align="center">
            Error:{" "}
            {isAxiosError(error) && error?.response
              ? (
                  error.response.data as { errors?: { message: string }[] }
                ).errors
                  ?.map((e) => e.message)
                  .join(", ")
              : "There was an unexpected error. Please try again."}
          </Typography>
        )}
      </Container>
    </Page>
  );
};

export default DemoPage;
