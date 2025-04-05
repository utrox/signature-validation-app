import { Container } from "@mui/material";

import Page from "../../components/Page";
import SignatureCanvas, {
  SignatureData,
} from "../../components/SignatureCanvas";
import useSignatureDemoValidationRequest from "../../requests/useSignatureDemoValidationRequest";
import { isAxiosError } from "axios"; // make sure you import this

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
      <Container>
        <h1>Demo Page</h1>

        {isPending ? (
          <p>Loading...</p>
        ) : (
          <SignatureCanvas onSave={addSignature} />
        )}

        {isSuccess && (
          <p>
            Congratulations! Your signature is either valid, or you're good at
            forging signatures.
          </p>
        )}

        {error && (
          <p style={{ color: "red" }}>
            Error: {isAxiosError(error) && error?.response ? error.response.data : "There was an unexpected error. Please try again."}
          </p>
        )}
      </Container>
    </Page>
  );
};

export default DemoPage;
