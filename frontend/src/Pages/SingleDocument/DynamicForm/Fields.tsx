import React from "react";
import {
  TextField,
  MenuItem,
  Checkbox,
  FormControlLabel,
  Radio,
  RadioGroup,
  FormControl,
  FormLabel,
  FormHelperText,
} from "@mui/material";
import { DatePicker, TimePicker } from "@mui/x-date-pickers";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";

import { FormInputValue, FormField } from "../../../types/dynamic_form";

interface FieldProps {
  field: FormField;
  onChange: (label: string, value: FormInputValue) => void;
}

const DynamicTextField: React.FC<FieldProps> = ({ field, onChange }) => {
  return (
    <TextField
      type={field.field_type}
      label={field.label}
      required={field.required}
      helperText={field.tooltip}
      fullWidth
      onChange={(e) => onChange(field.label, e.target.value)}
    />
  );
};

const DynamicChoiceField: React.FC<FieldProps> = ({ field, onChange }) => {
  return (
    <TextField
      select
      label={field.label}
      required={field.required}
      helperText={field.tooltip}
      fullWidth
      onChange={(e) => onChange(field.label, e.target.value)}
    >
      {field.choices.map((choice, index) => (
        <MenuItem key={index} value={choice}>
          {choice}
        </MenuItem>
      ))}
    </TextField>
  );
};

const DynamicCheckboxField: React.FC<FieldProps> = ({ field, onChange }) => {
  return (
    <>
      <FormControlLabel
        control={
          <Checkbox onChange={(e) => onChange(field.label, e.target.checked)} />
        }
        label={field.label}
      />
      <FormHelperText>{field.tooltip}</FormHelperText>
    </>
  );
};

const DynamicRadioField: React.FC<FieldProps> = ({ field, onChange }) => {
  return (
    <FormControl>
      <FormLabel>{field.label}</FormLabel>
      <RadioGroup onChange={(e) => onChange(field.label, e.target.value)}>
        {field.choices.map((choice, index) => (
          <FormControlLabel
            key={index}
            value={choice}
            control={<Radio />}
            label={choice}
          />
        ))}
      </RadioGroup>
      <FormHelperText>{field.tooltip}</FormHelperText>
    </FormControl>
  );
};

const DynamicDateField: React.FC<FieldProps> = ({ field, onChange }) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker
        label={field.label}
        onChange={(date) =>
          onChange(field.label, date ? date.format("YYYY-MM-DD") : "")
        }
      />
      <FormHelperText>{field.tooltip}</FormHelperText>
    </LocalizationProvider>
  );
};

const DynamicTimeField: React.FC<FieldProps> = ({ field, onChange }) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <TimePicker
        label={field.label}
        onChange={(time) =>
          onChange(field.label, time ? time.format("HH:mm") : "")
        }
        ampm={false}
      />
      <FormHelperText>{field.tooltip}</FormHelperText>
    </LocalizationProvider>
  );
};

const FieldRenderer: React.FC<FieldProps> = ({ field, onChange }) => {
  switch (field.field_type) {
    case "text":
    case "email":
    case "number":
    case "tel":
      return <DynamicTextField field={field} onChange={onChange} />;
    case "dropdown":
      return <DynamicChoiceField field={field} onChange={onChange} />;
    case "checkbox":
      return <DynamicCheckboxField field={field} onChange={onChange} />;
    case "radio":
      return <DynamicRadioField field={field} onChange={onChange} />;
    case "date":
      return <DynamicDateField field={field} onChange={onChange} />;
    case "time":
      return <DynamicTimeField field={field} onChange={onChange} />;
    default:
      return null;
  }
};

export default FieldRenderer;
