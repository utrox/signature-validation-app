import { ChangeEvent, useState } from "react";
import { List, Paper, TablePagination, TextField } from "@mui/material";
import DocumentRow from "./DocumentRow";
import useDocuments from "../../requests/useDocuments";

const DocumentTable = () => {
  const { documents, isLoading } = useDocuments();
  const [search, setSearch] = useState<string>("");
  const [page, setPage] = useState<number>(0);
  const [rowsPerPage, setRowsPerPage] = useState<number>(5);

  const filteredDocuments = documents
    ? documents.filter((doc) =>
        doc.name.toLowerCase().includes(search.toLowerCase())
      )
    : [];

  const handleChangePage = (_: unknown, newPage: number): void =>
    setPage(newPage);

  const handleChangeRowsPerPage = (
    event: ChangeEvent<HTMLInputElement>
  ): void => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <Paper sx={{ p: 2, mx: "auto", mt: 4 }}>
      <TextField
        label="Search by Name"
        variant="outlined"
        fullWidth
        value={search}
        onChange={(e: ChangeEvent<HTMLInputElement>) =>
          setSearch(e.target.value)
        }
        sx={{ mb: 2 }}
      />
      {isLoading && <div>Loading...</div>}
      {!isLoading && (
        <>
          <List>
            {filteredDocuments
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((document, index) => (
                <DocumentRow document={document} key={index} />
              ))}
          </List>
          <TablePagination
            component="div"
            count={filteredDocuments.length}
            page={page}
            rowsPerPage={rowsPerPage}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </>
      )}
    </Paper>
  );
};

export default DocumentTable;
