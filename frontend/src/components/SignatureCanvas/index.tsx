import { ReactSketchCanvas, ReactSketchCanvasRef } from "react-sketch-canvas";
import { Button, CircularProgress, Typography } from "@mui/material";
import React, { useEffect, useRef, useState } from "react";

const PHYSICAL_SIGNATURE_PLACE = import.meta.env.VITE_PHYSICAL_PLACE === "true";

export interface SignatureCanvasProps {
  onSave: (data: SignatureData) => void;
  isLoading?: boolean;
}

export type SignatureData = {
  imgData: string; // base64
  signatureTimeMs: number; // How long the signature drawing took place
};

const styles = {
  border: "0.0625rem solid #9c9c9c",
  borderRadius: "0.25rem",
  margin: "auto",
};

const SignatureCanvas: React.FC<SignatureCanvasProps> = ({
  onSave,
  isLoading,
}) => {
  const canvasRef = useRef<ReactSketchCanvasRef>(null);
  const [showSignatures, setShowSignatures] = useState<boolean>(true);

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

  const save = async () => {
    if (canvasRef.current) {
      const base64String = await canvasRef.current.exportImage("png");
      const signatureTime = await canvasRef.current.getSketchingTime();

      console.log("Saving...");
      onSave({
        imgData: base64String,
        signatureTimeMs: signatureTime,
      });
      canvasRef.current.resetCanvas();
    }
  };

  const clearCanvas = () => {
    if (canvasRef.current) canvasRef.current.resetCanvas();
  };

  if (!PHYSICAL_SIGNATURE_PLACE || !showSignatures)
    return (
      <Typography variant="h6" color="error" align="center">
        Please go to a terminal at a physical location to record your
        signatures. If you're already at a terminal, please resize your window
        to it's full width.
      </Typography>
    );

  return (
    <div
      style={{
        width: "fit-content",
        margin: "auto",
      }}
    >
      {isLoading ? (
        <div
          style={{
            textAlign: "center",
            height: "200px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <CircularProgress />
        </div>
      ) : (
        <>
          <ReactSketchCanvas
            ref={canvasRef}
            style={styles}
            width="600px"
            height="200px"
            strokeWidth={4}
            strokeColor="black"
            withTimestamp
          />
          <Button color="primary" onClick={save}>
            Save
          </Button>
          <Button color="error" onClick={clearCanvas}>
            Clear Board
          </Button>
        </>
      )}
    </div>
  );
};

export default SignatureCanvas;
