import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from "@mui/material";

import SignatureCanvas, {
  SignatureData,
} from "../../components/SignatureCanvas";
import React, { useEffect, useState } from "react";
import useSubmitSignatureForWorkflow from "../../requests/useSubmitSignatureForWorkflow";

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
    isSuccess,
    isError,
  } = useSubmitSignatureForWorkflow();
  const [signature, setSignature] = useState<SignatureData | null>(null);

  useEffect(() => {
    if (signature) {
      querySubmitDocumentSignature({ signature, workflowId });
    }
  }, [signature]);

  useEffect(() => {
    if (isSuccess || isError) onClose();
  }, [isSuccess, isError]);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>Sign Document</DialogTitle>
      <DialogContent>
        <SignatureCanvas
          onSave={(data: SignatureData) => {
            setSignature(data);
          }}
          isLoading={isPending}
        />
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
