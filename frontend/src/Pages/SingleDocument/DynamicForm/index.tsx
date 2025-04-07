import React, { useEffect, useState } from "react";
import { Button, ButtonGroup, Typography } from "@mui/material";

import FieldRenderer from "./Fields";
import {
  FormInputValue,
  DocumentData,
  FormState,
} from "../../../types/dynamic_form";

interface DynamicFormProps {
  formData: DocumentData;
  onSubmit: (formValues: FormState) => void;
  onPreview: (formValues: FormState) => void;
}

const DynamicForm: React.FC<DynamicFormProps> = ({
  formData,
  onSubmit,
  onPreview,
}) => {
  const [formValues, setFormValues] = useState<FormState>({});

  const handleChange = (field: string, value: FormInputValue) => {
    setFormValues((prev: FormState) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit(formValues);
  };

  const handlePreview = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    onPreview(formValues);
  };

  // An uncontrolled input should never be changed to be controlled.
  // Instead, we dynamically set the default data for the formValues state.
  // https://react.dev/reference/react-dom/components/input#controlling-an-input-with-a-state-variable
  useEffect(() => {
    const initialFormValues = formData?.form?.form_fields?.reduce(
      // If we add defaultValue functionality on admin later: current.defaultValue || ""
      (prev, current) => ({ ...prev, [current.field_id]: "" }),
      {}
    );
    setFormValues(initialFormValues);
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      {formData?.form?.form_fields?.map((field) => (
        <div key={field.id} style={{ marginBottom: "16px" }}>
          <FieldRenderer
            field={field}
            onChange={handleChange}
            value={formValues[field.field_id]}
          />
        </div>
      ))}
      {!formData?.form?.form_fields?.length && (
        <Typography variant="h6" style={{ marginBottom: "16px" }}>
          Good news! You don't need to provide any additional information for
          this document.
        </Typography>
      )}
      <ButtonGroup>
        <Button type="submit" variant="contained" color="primary">
          Submit
        </Button>
        <Button
          type="button"
          variant="outlined"
          color="secondary"
          onClick={handlePreview}
        >
          Preview
        </Button>
      </ButtonGroup>
    </form>
  );
};

export default DynamicForm;
