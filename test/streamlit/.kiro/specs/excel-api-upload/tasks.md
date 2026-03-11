# Implementation Plan: Excel API Upload

## Overview

Triển khai REST API endpoints để upload và xử lý file Excel cho báo cáo daily và weekly. Hệ thống sử dụng FastAPI, chạy trên port riêng biệt (8001), và tái sử dụng toàn bộ logic xử lý từ các module hiện tại mà không cần thay đổi.

## Tasks

- [ ] 1. Set up API project structure and dependencies
  - Create `api/` directory structure with modules
  - Add FastAPI and related dependencies to requirements.txt
  - Create configuration for API server (port, CORS, etc.)
  - _Requirements: 5.1, 5.2_

- [ ] 2. Implement core API server and routing
  - [ ] 2.1 Create FastAPI application with basic configuration
    - Implement `api/server.py` with ExcelAPIServer class
    - Set up CORS middleware and basic error handling
    - Configure logging and request tracking
    - _Requirements: 1.1, 1.2, 6.2_

  - [ ]* 2.2 Write property test for API server initialization
    - **Property 13: System Isolation**
    - **Validates: Requirements 5.3, 5.5**

  - [ ] 2.3 Implement API routing and health endpoint
    - Create `/api/daily/upload` and `/api/weekly/upload` endpoints
    - Implement `/health` endpoint for monitoring
    - Set up request validation middleware
    - _Requirements: 1.1, 1.2_

  - [ ]* 2.4 Write unit tests for API endpoints
    - Test health endpoint availability
    - Test endpoint routing and basic validation
    - _Requirements: 1.1, 1.2_

- [ ] 3. Implement file handling and validation
  - [ ] 3.1 Create FileHandler class with validation logic
    - Implement file format validation (xlsx, xls)
    - Add file size validation (50MB limit)
    - Implement MIME type checking
    - _Requirements: 2.1, 2.2, 8.1_

  - [ ]* 3.2 Write property test for file format validation
    - **Property 1: File Format Validation**
    - **Validates: Requirements 2.1, 8.1**

  - [ ] 3.3 Implement secure temporary file management
    - Create secure temporary directory handling
    - Implement file cleanup mechanisms
    - Add automatic cleanup on timeout/error
    - _Requirements: 2.5, 8.4, 8.5_

  - [ ]* 3.4 Write property test for secure file lifecycle
    - **Property 2: Secure File Lifecycle Management**
    - **Validates: Requirements 2.5, 8.5**

  - [ ] 3.5 Add security scanning and rate limiting
    - Implement basic malicious content detection
    - Add rate limiting middleware
    - Implement request throttling
    - _Requirements: 8.2, 8.3_

  - [ ]* 3.6 Write property tests for security features
    - **Property 20: Malicious Content Detection**
    - **Property 21: Rate Limiting Enforcement**
    - **Validates: Requirements 8.2, 8.3**

- [ ] 4. Checkpoint - Ensure file handling tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Daily Service integration
  - [ ] 5.1 Create DailyService class with existing module integration
    - Import and integrate ReportGenerator from report_generator.py
    - Implement 24-hour window calculation logic
    - Create interface for daily report processing
    - _Requirements: 3.1, 3.2_

  - [ ]* 5.2 Write property test for daily time window calculation
    - **Property 7: Daily Time Window Calculation**
    - **Validates: Requirements 3.2**

  - [ ] 5.3 Implement daily slide generation workflow
    - Integrate with existing slide generators (6 slides)
    - Implement data processing pipeline
    - Add error handling for processing failures
    - _Requirements: 3.3_

  - [ ]* 5.4 Write property test for daily slide generation
    - **Property 8: Daily Slide Generation**
    - **Validates: Requirements 3.3**

  - [ ] 5.5 Implement daily prompt generation
    - Integrate with existing prompt generation logic
    - Create complete prompt text from processed data
    - Add metadata and structured data output
    - _Requirements: 3.4_

  - [ ]* 5.6 Write property test for prompt generation
    - **Property 12: Prompt Generation Completeness**
    - **Validates: Requirements 3.4**

- [ ] 6. Implement Weekly Service integration
  - [ ] 6.1 Create WeeklyService class with existing module integration
    - Import and integrate WeeklyReportGenerator from report_generator_weekly.py
    - Implement weekly window calculation logic
    - Create interface for weekly report processing
    - _Requirements: 4.1, 4.2_

  - [ ]* 6.2 Write property test for weekly time window calculation
    - **Property 9: Weekly Time Window Calculation**
    - **Validates: Requirements 4.2**

  - [ ] 6.3 Implement weekly slide generation workflow
    - Integrate with existing weekly slide generators (12 slides)
    - Implement weekly data processing pipeline
    - Add error handling for weekly processing
    - _Requirements: 4.3_

  - [ ]* 6.4 Write property test for weekly slide generation
    - **Property 10: Weekly Slide Generation**
    - **Validates: Requirements 4.3**

  - [ ] 6.5 Implement weekly prompt generation
    - Integrate with existing weekly prompt logic
    - Create complete weekly prompt text
    - Add weekly metadata and structured output
    - _Requirements: 4.4_

- [ ] 7. Implement request/response handling
  - [ ] 7.1 Create Pydantic models for request validation
    - Implement DailyUploadRequest and WeeklyUploadRequest models
    - Add field validation (date formats, brand name, etc.)
    - Create file upload validation models
    - _Requirements: 1.4, 1.5_

  - [ ]* 7.2 Write property test for parameter validation
    - **Property 6: Invalid Parameter Error Handling**
    - **Validates: Requirements 1.5, 2.4**

  - [ ] 7.3 Create ResponseFormatter class
    - Implement consistent JSON response formatting
    - Add success and error response structures
    - Include metadata (processing_time, request_id)
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [ ]* 7.4 Write property test for response format consistency
    - **Property 15: Response Format Consistency**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5**

- [ ] 8. Checkpoint - Ensure service integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement comprehensive error handling
  - [ ] 9.1 Create error classification and HTTP status mapping
    - Implement error categories (400, 500, 503)
    - Add appropriate HTTP status code mapping
    - Create detailed error message formatting
    - _Requirements: 6.1, 6.3, 6.5_

  - [ ]* 9.2 Write property test for error status codes
    - **Property 16: Error Status Code Mapping**
    - **Validates: Requirements 6.1, 6.3**

  - [ ] 9.3 Implement timeout and graceful error handling
    - Add timeout handling for long-running processes
    - Implement graceful degradation for LLM API failures
    - Add retry mechanisms for transient failures
    - _Requirements: 6.4_

  - [ ]* 9.4 Write property test for timeout handling
    - **Property 18: Graceful Timeout Handling**
    - **Validates: Requirements 6.4**

  - [ ] 9.5 Implement comprehensive logging system
    - Add request logging with timestamps and file info
    - Implement processing status tracking
    - Add detailed error logging for debugging
    - _Requirements: 6.2, 6.5_

  - [ ]* 9.6 Write property test for request logging
    - **Property 17: Comprehensive Request Logging**
    - **Validates: Requirements 6.2**

- [ ] 10. Wire all components together
  - [ ] 10.1 Create main API application entry point
    - Implement `api_main.py` with server startup logic
    - Wire all services and handlers together
    - Add environment configuration loading
    - _Requirements: 5.4_

  - [ ]* 10.2 Write property test for configuration consistency
    - **Property 14: Configuration Consistency**
    - **Validates: Requirements 5.4**

  - [ ] 10.3 Implement complete request processing pipeline
    - Connect file upload → validation → processing → response
    - Add end-to-end error handling
    - Implement cleanup on all exit paths
    - _Requirements: 1.3, 2.4, 3.5, 4.5_

  - [ ]* 10.4 Write property test for multipart form data handling
    - **Property 5: Multipart Form Data Acceptance**
    - **Validates: Requirements 1.3, 1.4**

- [ ] 11. Create deployment and startup scripts
  - [ ] 11.1 Create API server startup script
    - Implement `run_api.sh` for development
    - Add production deployment configuration
    - Create Docker configuration for API server
    - _Requirements: 5.1_

  - [ ] 11.2 Add API server to existing Docker setup
    - Update docker-compose files to include API service
    - Configure port mapping and environment variables
    - Ensure API runs independently from Streamlit
    - _Requirements: 5.1, 5.3_

- [ ] 12. Final integration and testing
  - [ ] 12.1 Implement end-to-end integration tests
    - Test complete upload → process → response workflow
    - Test concurrent request handling
    - Verify no interference with Streamlit app
    - _Requirements: 5.3, 5.5_

  - [ ]* 12.2 Write property test for processing logic reuse
    - **Property 11: Processing Logic Reuse**
    - **Validates: Requirements 3.1, 4.1**

  - [ ] 12.3 Performance and load testing
    - Test with various file sizes and data volumes
    - Verify memory usage and cleanup
    - Test rate limiting under load
    - _Requirements: 2.2, 8.3_

- [ ] 13. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation and user feedback
- Property tests validate universal correctness properties using `hypothesis` library
- Unit tests validate specific examples and edge cases
- All existing modules (report_generator.py, slide_generators.py, etc.) are reused without modification
- API server runs on port 8001, separate from Streamlit on port 8501
- Environment variables are shared between Streamlit and API for consistency