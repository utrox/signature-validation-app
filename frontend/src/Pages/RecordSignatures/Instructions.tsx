import { Typography } from "@mui/material";

const RecordSignatureInstructions = () => {
  return (
    <>
      <Typography variant="h5" gutterBottom>
        Signature Registration
      </Typography>
      <Typography variant="body1" align="center" paragraph>
        Welcome to the Signature Registration page! Please use the touchscreen
        or tablet to create your signature below, exactly as you would on a
        legal document. This signature will be used to verify your identity in
        future transactions.
      </Typography>

      <Typography variant="body1" align="center" paragraph>
        Don't worry! You can take as many practice signatures as you'd like! You
        can always reset your current signature by pressing Clear Canvas. Take
        your time to ensure each signature reflects your usual signature style –
        smooth and authentic. Please make sure you only submit signatures you're
        satisfied with.
      </Typography>
    </>
  );
};

export default RecordSignatureInstructions;
