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
  value: FormInputValue;
}

type DynamicFieldType = React.FC<FieldProps>;

const DynamicTextField: DynamicFieldType = ({ field, onChange, value }) => {
  return (
    <TextField
      type={field.field_type}
      label={field.label}
      required={field.required}
      helperText={field.tooltip}
      fullWidth
      value={value}
      onChange={(e) => onChange(field.field_id, e.target.value)}
    />
  );
};

const DynamicChoiceField: DynamicFieldType = ({ field, onChange, value }) => {
  return (
    <TextField
      select
      label={field.label}
      required={field.required}
      helperText={field.tooltip}
      fullWidth
      value={value}
      onChange={(e) => onChange(field.field_id, e.target.value)}
    >
      {field.choices.map((choice, index) => (
        <MenuItem key={index} value={choice}>
          {choice}
        </MenuItem>
      ))}
    </TextField>
  );
};

const DynamicCheckboxField: DynamicFieldType = ({ field, onChange, value }) => {
  return (
    <>
      <FormControlLabel
        control={
          <Checkbox
            checked={!!value}
            onChange={(e) => onChange(field.label, e.target.checked)}
          />
        }
        label={field.label}
      />
      <FormHelperText>{field.tooltip}</FormHelperText>
    </>
  );
};

// TODO: solve checkboxes with multiple values?
const DynamicRadioField: DynamicFieldType = ({ field, onChange, value }) => {
  return (
    <FormControl>
      <FormLabel>{field.label}</FormLabel>
      <RadioGroup
        onChange={(e) => onChange(field.field_id, e.target.value)}
        value={value}
      >
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

const DynamicDateField: DynamicFieldType = ({ field, onChange }) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker
        label={field.label}
        onChange={(date) =>
          onChange(field.field_id, date ? date.format("YYYY-MM-DD") : "")
        }
      />
      <FormHelperText>{field.tooltip}</FormHelperText>
    </LocalizationProvider>
  );
};

const DynamicTimeField: DynamicFieldType = ({ field, onChange }) => {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <TimePicker
        label={field.label}
        onChange={(time) =>
          onChange(field.field_id, time ? time.format("HH:mm") : "")
        }
        ampm={false}
      />
      <FormHelperText>{field.tooltip}</FormHelperText>
    </LocalizationProvider>
  );
};

const FieldRenderer: DynamicFieldType = ({ field, onChange, value = "" }) => {
  switch (field.field_type) {
    case "text":
    case "email":
    case "number":
    case "tel":
      return (
        <DynamicTextField field={field} onChange={onChange} value={value} />
      );
    case "dropdown":
      return (
        <DynamicChoiceField field={field} onChange={onChange} value={value} />
      );
    case "checkbox":
      return (
        <DynamicCheckboxField field={field} onChange={onChange} value={value} />
      );
    case "radio":
      return (
        <DynamicRadioField field={field} onChange={onChange} value={value} />
      );
    case "date":
      return (
        <DynamicDateField field={field} onChange={onChange} value={value} />
      );
    case "time":
      return (
        <DynamicTimeField field={field} onChange={onChange} value={value} />
      );
    default:
      return null;
  }
};

export default FieldRenderer;
