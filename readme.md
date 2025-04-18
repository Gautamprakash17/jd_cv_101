Endpoint         | Method    | Description
/extract         | POST      | Extract candidate details from a single CV (PDF)
/score           | POST      | Compare JD and CV, return a numeric match score (0-100)
/process-batch   | POST      | Upload JD + multiple CVs, extract & score all, save Excel
/download-excel  | GET       | Download the final compiled Excel file