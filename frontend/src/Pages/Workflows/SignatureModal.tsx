import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
} from "@mui/material";

import SignatureCanvas, {
  SignatureData,
} from "../../components/SignatureCanvas";
import React, { useEffect, useState } from "react";
import useSubmitSignatureForWorkflow from "../../requests/useSubmitSignatureForWorkflow";

const PHYSICAL_SIGNATURE_PLACE = import.meta.env.VITE_PHYSICAL_PLACE === "true";

interface SignatureModalProps {
  workflowId: string;
  open: boolean;
  onClose: () => void;
}

const SignatureModal: React.FC<SignatureModalProps> = ({
  workflowId,
  open,
  onClose,
}) => {
  const {
    mutate: querySubmitDocumentSignature,
    isPending,
  } = useSubmitSignatureForWorkflow();
  const [signature, setSignature] = useState<SignatureData | null>(null);
  const [showSignatures, setShowSignatures] = useState(true);
  // Don't let them resize the window under 700px and still use the signature function.
  const handleResize = () => {
    setShowSignatures(window.innerWidth >= 700);
  };

  useEffect(() => {
    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  useEffect(() => {
    if (signature) {
      querySubmitDocumentSignature({ signature, workflowId });
      onClose();
    }
  }, [signature]);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Sign Document</DialogTitle>
      <DialogContent>
        {!PHYSICAL_SIGNATURE_PLACE || !showSignatures ? (
          <Typography variant="h6" color="error" align="center">
            Please go to a terminal at a physical location to record your
            signatures. If you're already at a terminal, please resize your
            window to it's full width.
          </Typography>
        ) : isPending ? (
          <div>Loading</div>
        ) : (
          <SignatureCanvas
            onSave={(data: SignatureData) => {
              setSignature(data);
            }}
          />
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="inherit">
          Cancel
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default SignatureModal;
