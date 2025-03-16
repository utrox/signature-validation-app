import React, { useEffect, useState } from "react";
import { Button } from "@mui/material";

import FieldRenderer from "./Fields";
import {
  FormInputValue,
  DocumentData,
  FormState,
} from "../../../types/dynamic_form";

interface DynamicFormProps {
  formData: DocumentData;
  onSubmit: (formValues: FormState) => void;
}

const DynamicForm: React.FC<DynamicFormProps> = ({ formData, onSubmit }) => {
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

  // An uncontrolled input should never be changed to be controlled.
  // Instead, we dynamically set the default data for the formValues state.
  // https://react.dev/reference/react-dom/components/input#controlling-an-input-with-a-state-variable
  useEffect(() => {
    const initialFormValues = formData?.form?.form_fields?.reduce(
      // If we add defaultValue functionality on admin later: current.defaultValue || ""
      (prev, current) => ({ ...prev, [current.label]: "" }), 
      {}
    );
    setFormValues(initialFormValues);
  }, []);

  return (
    <form onSubmit={handleSubmit}>
      {formData?.form?.form_fields?.map((field) => (
        <div key={field.id} style={{ marginBottom: "16px" }}>
          <FieldRenderer field={field} onChange={handleChange} />
        </div>
      ))}
      <Button type="submit" variant="contained" color="primary">
        Submit
      </Button>
    </form>
  );
};

export default DynamicForm;
