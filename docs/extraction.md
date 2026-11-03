## 1. DATA SOURCE AND EXTRACTION SPECIFICATION

### 1.1 Source System

The data warehouse will obtain student performance data from faculty-provided records and survey-generated datasets. These datasets serve as external data sources because the proposed system does not directly connect to the existing institutional student information system.

### 1.2 Source Database/File

The primary source files are expected to be Excel and CSV files containing student performance and survey data. SQLite databases may also be accepted as an alternative source format. If the source data is stored in SQLite, a Python-based conversion utility may be used to export the data into Excel or CSV format without altering the original SQLite database.

### 1.3 Extraction Method

The system will use a full extraction approach. All available records from the submitted source file will be extracted during each data collection period. Extraction will generally occur at the end of a semester or approximately every four months. Full extraction is appropriate because the source data is collected periodically rather than continuously from an operational system.

### 1.4 Extraction Scope

The extraction process will retrieve all student performance records available in the submitted source files. A record must contain the required attributes `sr-code`, `grades`, `year`, `section`, and `subject`. These fields will be used to identify students, evaluate academic performance, analyze performance by year level, section, and subject, and detect potential duplicate records.

| Column | Purpose |
|---|---|
| `sr-code` | Unique student identifier used for student identification and duplicate detection |
| `grades` | Primary measure of student academic performance |
| `year` | Used to analyze performance by year level |
| `section` | Used to compare performance between sections |
| `subject` | Used to identify subjects where students may be experiencing difficulty |

### 1.5 Source Limitation and Assumption

The proposed data warehouse does not directly extract data from the institution's operational information system. Instead, it relies on manually provided Excel, CSV, or SQLite files obtained from faculty members and surveys. Consequently, the quality, completeness, consistency, and accuracy of the warehouse depend on the quality of the submitted source data.

The extraction process requires the presence of the predefined required headers. Files with missing required fields may be rejected. The system will, however, attempt to accommodate differences in column ordering and variations in the location of the header row.

A **0.3% tolerance** for detected duplicate or invalid records will be applied per extraction batch. Records identified as duplicates or invalid within this tolerance may be flagged for review while allowing the remaining valid records to proceed through the extraction process. If the number of problematic records exceeds the 0.3% tolerance, the extraction batch will require further validation or correction before it is loaded into the data warehouse.

## 2. SOURCE TABLES AND COLUMN SPECIFICATION

The `student_grade_profile` table contains student academic performance records and serves as the primary source of grade-related data for the data warehouse. The table provides the measurements necessary to analyze student performance and identify areas that may require academic attention.

The `grades` column stores the student's academic grade as a decimal value with two decimal places. The `year`, `section`, and `subject` columns provide the classification and academic context of each performance record. These attributes are important for analyzing performance across different year levels, sections, and subjects and for identifying areas where students may require additional academic attention.

| Column | Data Type | Description |
|---|---|---|
| `sr_code` | VARCHAR | Unique identifier of the student |
| `grades` | DECIMAL(4,2) | Student's academic grade, stored with two decimal places |
| `year` | INTEGER | Year level of the student |
| `section` | VARCHAR | Section in which the student is enrolled |
| `subject` | VARCHAR | Subject associated with the recorded grade |

## 3. EXTRACTION VALIDATION AND DATA QUALITY CHECKS

| Check Name | Target | Purpose | Validation Criteria |
|---|---|---|---|
| **V1 - Null Checks** | All required columns | To identify missing values in required fields | Error rate should not be greater than **10%**. Records containing null values are logged and flagged for review. |
| **V2 - Data Type Checks** | `grades`, `year` | To ensure values use the expected data types and prevent data type inconsistency | Error rate should not be greater than **0.2%**. If exceeded, the batch is flagged as **Unhealthy**. Otherwise, invalid rows are logged and quarantined. |
| **V3 - Domain/Value Checks** | `grades`, `year`, `subject` | To ensure values are within the expected values or format based on the approved sample/reference data | Error rate should not be greater than **0.2%**. Invalid rows are logged and quarantined. |
| **V4 - Duplicate Checks** | `sr_code`, `year`, `subject` | To identify duplicate academic performance records | Duplicate rate should not exceed **0.3%**. Duplicate rows are logged and quarantined for review. |
| **V5 - SR-Code Format Check** | `sr_code` | To ensure the student identifier follows the expected format | Invalid `sr_code` records should not exceed **0.2%**. Invalid rows are logged and quarantined. |
| **V6 - Grade Range Check** | `grades` | To ensure grades fall within the accepted grading scale | Any grade outside the defined grading range is considered invalid and quarantined. |
| **V7 - Year Level Check** | `year` | To ensure the year level contains only valid year levels | Values outside the approved year-level values are invalid and quarantined. |
| **V8 - Subject Completeness Check** | `subject` | To ensure every performance record is associated with a valid subject | Missing or unrecognized subjects are logged and quarantined. |
| **V9 - Section Validation** | `section` | To ensure the section value follows the expected format or belongs to an approved section list | Invalid or unrecognized sections are logged and quarantined. |
| **V10 - Header/Schema Check** | Source file | To ensure all required columns are present before extraction | If any required column is missing, the extraction is rejected. Column order and header-row position may vary. |
| **V11 - Record Count Check** | Entire batch | To detect unexpected loss or increase of records during extraction/transformation | Extracted record count must match the source record count unless explicitly excluded records are documented. |
| **V12 - Referential Integrity Check** | Related tables | To ensure records reference valid students, subjects, sections, etc. | Records with invalid references are flagged and quarantined. |
| **V13 - Whitespace/Format Check** | `sr_code`, `subject`, `section` | To detect unnecessary spaces, inconsistent capitalization, or formatting differences | Values are normalized before validation; unresolved inconsistencies are logged. |
| **V14 - Encoding/Character Check** | Text columns | To identify unreadable or corrupted characters from Excel/CSV files | Records containing invalid or unreadable characters are flagged for review. |
| **V15 - Outlier/Anomaly Check** | `grades` | To identify unusual grade patterns that may indicate data-entry errors | Suspicious values are flagged for review rather than automatically rejected. |

## 4. Extraction Metadata and Log Specification

the pipeline run id, file name, 

the logs will be first date, second pipeline run id, file name, 

## 5. Log Retention and Access

The system maintains logs for the **system, extraction, transformation, and loading (ETL)** processes. These logs are stored in the project's `logs/` folder and can be accessed by anyone who has access to the project files.

### Log Retention

Logs are retained for **90 days** by default. Logs older than the 90-day retention period can be removed by running the following command from the project root:

```bash
clean-logs
```

The `clean-logs` command applies the retention policy to the following log categories:

- System logs
- Extraction logs
- Transformation logs
- Loading logs

This allows the project to automatically remove outdated logs and prevent unnecessary growth of the log directory.

### Log Archiving

Logs that need to be retained beyond the 90-day period can be explicitly archived using the following command:

```bash
logs <log-id's>
```

The specified log IDs will be collected and saved as an archive file. The archive will be stored separately from the active logs using the following naming convention:

```text
archived-[date].logs
```

For example:

```text
archived-2026-11-03.logs
```

Archived logs are not affected by the regular 90-day cleanup process and can therefore be retained for future reference, auditing, or troubleshooting.