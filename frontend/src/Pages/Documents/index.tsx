import "./documents.css";

import React, { useState, ChangeEvent } from "react";
import { Link } from "react-router-dom";
import {
  TextField,
  List,
  ListItem,
  ListItemText,
  Paper,
  TablePagination,
  IconButton,
  Tooltip,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import useDocuments from "../../requests/useDocuments";
import Page from "../../components/Page";

const Document: React.FC = () => {
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
    <Page title="Documents">
      <Paper sx={{ p: 2, maxWidth: 400, mx: "auto", mt: 4 }}>
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
        {/* TODO: loading component */}
        {isLoading && <div>Loading...</div>}
        {!isLoading && (
          <>
            <List>
              {filteredDocuments
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((document, index) => (
                  <Link to={`/documents/${document.id}`}>
                    <ListItem key={index} className="doc-list-item">
                      <ListItemText primary={document.name} />
                      <Tooltip title="View">
                        <IconButton>
                          <VisibilityIcon color="primary" />
                        </IconButton>
                      </Tooltip>
                    </ListItem>
                  </Link>
                ))}
            </List>
            {/* TODO: more filtering? like having multiple DocumentCategories or smth. */}
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
    </Page>
  );
};

export default Document;
