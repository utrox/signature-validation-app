/* 
Types for data from the backend, used
for rendering out the dynamic form.
*/
export type DocumentData = {
  id: number;
  name: string;
  form: {
    id: number;
    document: number;
    description: string;
    form_fields: FormField[];
  };
};

export type FormField = {
  id: number;
  label: string;
  tooltip: string;
  field_type: FieldTypes;
  required: boolean;
  order: number;
  choices: string[];
};

export type FieldTypes =
  | "text"
  | "number"
  | "email"
  | "date"
  | "time"
  | "tel"
  | "dropdown"
  | "checkbox"
  | "file"
  | "radio";

/* Types for state management and user responses. */
export type FormInputValue = string | boolean;
export interface FormState {
  [key: string]: FormInputValue;
}
