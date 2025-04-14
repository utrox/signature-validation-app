
export const addHiddenField = (
  form: HTMLFormElement,
  name: string,
  value: string
) => {
  const formDataField = document.createElement("input");
  formDataField.type = "hidden";
  formDataField.name = name;
  formDataField.value = value;
  form.appendChild(formDataField);
};
