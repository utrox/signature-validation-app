import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Typography,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from "@mui/material";
import { Dayjs } from "dayjs";
import { useState } from "react";
import { Box } from "@mui/system";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { useEffect } from "react";
import { KeyboardDoubleArrowDown } from "@mui/icons-material";

import { WorkflowData, WORKFLOW_STATUSES } from "./types";

interface FilterResultsProps {
  workflows: WorkflowData[];
  setFiltered: React.Dispatch<React.SetStateAction<WorkflowData[]>>;
}

const FilterResults: React.FC<FilterResultsProps> = ({
  workflows,
  setFiltered,
}) => {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [dateFrom, setDateFrom] = useState<Dayjs | null>(null);
  const [dateTo, setDateTo] = useState<Dayjs | null>(null);

  useEffect(() => {
    let temp = [...workflows];

    if (search) {
      temp = temp.filter((wf) =>
        wf.document_name.toLowerCase().includes(search.toLowerCase())
      );
    }

    if (statusFilter) {
      temp = temp.filter((wf) => wf.status === statusFilter);
    }

    if (dateFrom) {
      temp = temp.filter((wf) => {
        const date = dayjs(wf.created_at);
        return date.isAfter(dateFrom.startOf("day"));
      });
    }

    if (dateTo) {
      temp = temp.filter((wf) => {
        const date = dayjs(wf.created_at);
        return date.isBefore(dayjs(dateTo).endOf("day"));
      });
    }

    setFiltered(temp);
  }, [search, statusFilter, dateFrom, dateTo, workflows]);

  return (
    <Accordion color="primary" sx={{ mb: 2, borderRadius: 2 }}>
      <AccordionSummary
        expandIcon={
          <KeyboardDoubleArrowDown
            sx={{
              color: (theme) => theme.palette.primary.contrastText,
              borderRadius: 2,
            }}
          />
        }
        aria-controls="panel1-content"
        id="panel1-header"
        sx={{
          backgroundColor: (theme) => theme.palette.primary.dark,
          color: (theme) => theme.palette.primary.contrastText,
          "&:hover": {
            backgroundColor: (theme) => theme.palette.primary.main,
          },
          borderRadius: 2,
          "&.Mui-expanded": {
            borderEndStartRadius: 0,
            borderEndEndRadius: 0,
          },
        }}
      >
        <Typography component="span">Filter Result</Typography>
      </AccordionSummary>
      <AccordionDetails>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr", // mobile: single column
              sm: "1fr 1fr", // Above xs size (600px): 2 columns
            },
            gap: 2,
          }}
        >
          <TextField
            label="Search Document by Name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>Status</InputLabel>
            <Select
              label="Status"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <MenuItem value="">All</MenuItem>
              {(
                Object.keys(WORKFLOW_STATUSES) as Array<
                  keyof typeof WORKFLOW_STATUSES
                >
              ).map((key) => (
                <MenuItem key={key} value={key}>
                  {WORKFLOW_STATUSES[key].label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Typography gridColumn={"span 2"}>
            Creation Date
          </Typography>
          <LocalizationProvider
            dateAdapter={AdapterDayjs}
            adapterLocale="zh-cn"
          >
            <DatePicker
              value={dateFrom}
              onChange={(newDate) => setDateFrom(newDate)}
              label="Creation From"
            />
            <DatePicker
              value={dateTo}
              onChange={(newDate) => setDateTo(newDate)}
              label="Creation To"
            />
          </LocalizationProvider>
        </Box>
      </AccordionDetails>
    </Accordion>
  );
};

export default FilterResults;
