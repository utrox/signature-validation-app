import { ReactSketchCanvas, ReactSketchCanvasRef } from "react-sketch-canvas";
import { Button } from "@mui/material";
import React, { useRef } from "react";

export interface SignatureCanvasProps {
  onSave: (data: SignatureData) => void;
}

export type SignatureData = {
    imgData: string; // base64
    signatureTimeMs: number; // How long the signature drawing took place
  };

const styles = {
  border: "0.0625rem solid #9c9c9c",
  borderRadius: "0.25rem",
};

const SignatureCanvas: React.FC<SignatureCanvasProps> = ({onSave}) => {
  const canvasRef = useRef<ReactSketchCanvasRef>(null);

  return (
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

      <Button
        color="primary"
        onClick={async () => {
          if (canvasRef.current) {
            const base64String = await canvasRef.current.exportImage("png");
            const signatureTime = await canvasRef.current.getSketchingTime();

            onSave({
              imgData: base64String,
              signatureTimeMs: signatureTime,
            });
            canvasRef.current.resetCanvas();
          }
        }}
      >
        Save
      </Button>
      <Button
        color="error"
        onClick={() => {
          if (canvasRef.current) canvasRef.current.resetCanvas();
        }}
      >
        Clear Board
      </Button>
    </>
  );
};

export default SignatureCanvas;
