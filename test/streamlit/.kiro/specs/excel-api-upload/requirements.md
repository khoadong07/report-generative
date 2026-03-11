# Requirements Document

## Introduction

Tính năng Excel API Upload cho phép người dùng upload file Excel thông qua REST API endpoints để xử lý và tạo ra prompt cho báo cáo daily và weekly. Tính năng này sẽ tích hợp với hệ thống hiện tại mà không làm gián đoạn luồng Streamlit đang hoạt động.

## Glossary

- **Excel_API_System**: Hệ thống API endpoints để xử lý upload file Excel
- **Daily_Processor**: Module xử lý file Excel cho báo cáo daily (24h window)
- **Weekly_Processor**: Module xử lý file Excel cho báo cáo weekly
- **Prompt_Generator**: Component tạo ra prompt từ dữ liệu đã xử lý
- **Streamlit_App**: Ứng dụng web hiện tại đang chạy
- **File_Handler**: Component xử lý và validate file Excel
- **Response_Formatter**: Component format response trả về cho client

## Requirements

### Requirement 1: Excel Upload API Endpoints

**User Story:** Là một developer, tôi muốn có API endpoints để upload file Excel, để có thể tích hợp với các hệ thống khác mà không phụ thuộc vào Streamlit interface.

#### Acceptance Criteria

1. THE Excel_API_System SHALL provide a POST endpoint `/api/daily/upload` for daily report processing
2. THE Excel_API_System SHALL provide a POST endpoint `/api/weekly/upload` for weekly report processing
3. WHEN a valid Excel file is uploaded, THE Excel_API_System SHALL accept multipart/form-data requests
4. THE Excel_API_System SHALL accept additional parameters: brand_name, report_date, report_time
5. WHEN invalid parameters are provided, THE Excel_API_System SHALL return HTTP 400 with descriptive error messages

### Requirement 2: File Processing and Validation

**User Story:** Là một user, tôi muốn hệ thống validate file Excel trước khi xử lý, để đảm bảo dữ liệu đầu vào chính xác.

#### Acceptance Criteria

1. WHEN a file is uploaded, THE File_Handler SHALL validate file format (xlsx, xls)
2. WHEN file size exceeds 50MB, THE File_Handler SHALL reject the file with error message
3. THE File_Handler SHALL validate required Excel columns exist
4. IF file validation fails, THEN THE Excel_API_System SHALL return HTTP 400 with specific validation errors
5. THE File_Handler SHALL create temporary files securely and clean up after processing

### Requirement 3: Daily Report Processing

**User Story:** Là một user, tôi muốn upload file Excel để tạo daily report, để có thể tự động hóa quy trình tạo báo cáo hàng ngày.

#### Acceptance Criteria

1. WHEN `/api/daily/upload` receives a valid request, THE Daily_Processor SHALL process the Excel file using existing daily logic
2. THE Daily_Processor SHALL calculate 24-hour window based on report_date and report_time parameters
3. THE Daily_Processor SHALL generate 6 slides data (overview, trendline, channels, sentiment, top posts, deleted posts)
4. THE Prompt_Generator SHALL create complete prompt text from processed data
5. THE Response_Formatter SHALL return JSON response with prompt text and structured data

### Requirement 4: Weekly Report Processing

**User Story:** Là một user, tôi muốn upload file Excel để tạo weekly report, để có thể tự động hóa quy trình tạo báo cáo hàng tuần.

#### Acceptance Criteria

1. WHEN `/api/weekly/upload` receives a valid request, THE Weekly_Processor SHALL process the Excel file using existing weekly logic
2. THE Weekly_Processor SHALL calculate weekly window based on report_date parameter
3. THE Weekly_Processor SHALL generate 12 slides data for weekly report
4. THE Prompt_Generator SHALL create complete weekly prompt text from processed data
5. THE Response_Formatter SHALL return JSON response with prompt text and structured data

### Requirement 5: Non-Disruptive Integration

**User Story:** Là một system administrator, tôi muốn API hoạt động độc lập với Streamlit, để đảm bảo không ảnh hưởng đến người dùng hiện tại.

#### Acceptance Criteria

1. THE Excel_API_System SHALL run on separate port from Streamlit application
2. THE Excel_API_System SHALL reuse existing processing modules without modification
3. THE Streamlit_App SHALL continue to function normally when API is running
4. THE Excel_API_System SHALL use same environment variables and configuration as Streamlit
5. WHERE API server fails, THE Streamlit_App SHALL remain unaffected

### Requirement 6: Error Handling and Logging

**User Story:** Là một developer, tôi muốn có error handling và logging chi tiết, để có thể debug và monitor hệ thống hiệu quả.

#### Acceptance Criteria

1. WHEN processing errors occur, THE Excel_API_System SHALL return appropriate HTTP status codes
2. THE Excel_API_System SHALL log all requests with timestamp, file info, and processing status
3. IF LLM API calls fail, THEN THE Excel_API_System SHALL return HTTP 503 with retry information
4. THE Excel_API_System SHALL handle timeout scenarios gracefully
5. THE Excel_API_System SHALL provide detailed error messages for debugging

### Requirement 7: Response Format Standardization

**User Story:** Là một API consumer, tôi muốn có response format nhất quán, để có thể dễ dàng tích hợp và xử lý dữ liệu.

#### Acceptance Criteria

1. THE Response_Formatter SHALL return JSON responses with consistent structure
2. WHEN processing succeeds, THE Response_Formatter SHALL include: prompt_text, slide_data, metadata
3. WHEN errors occur, THE Response_Formatter SHALL include: error_code, error_message, details
4. THE Response_Formatter SHALL include processing_time and request_id for tracking
5. THE Response_Formatter SHALL set appropriate Content-Type headers

### Requirement 8: Security and File Handling

**User Story:** Là một security administrator, tôi muốn đảm bảo file upload được xử lý an toàn, để tránh các lỗ hổng bảo mật.

#### Acceptance Criteria

1. THE File_Handler SHALL validate file extensions and MIME types
2. THE File_Handler SHALL scan for malicious content in uploaded files
3. THE Excel_API_System SHALL implement rate limiting for upload requests
4. THE File_Handler SHALL store temporary files in secure directory with restricted permissions
5. THE File_Handler SHALL automatically delete temporary files after processing completion or timeout