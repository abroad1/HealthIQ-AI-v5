/**
 * TypeScript types for parsed lab data and upload functionality
 * Mirrors backend parse payloads and response structures
 */

export interface ParsedBiomarker {
  /** Biomarker name (e.g., "Total Cholesterol") */
  name: string;
  
  /** Numeric or string value */
  value: number | string;
  
  /** Unit of measurement (e.g., "mg/dL", "mmol/L") */
  unit: string;
  
  /** Processing status of this biomarker */
  status?: "raw" | "edited" | "confirmed";
}

export interface ParseMetadata {
  /** Unique analysis identifier */
  analysis_id: string;
  
  /** Timestamp of parsing */
  timestamp: string;
  
  /** Source type (file upload vs text input) */
  source_type: "lab_report" | "text_input" | "unknown";
  
  /** Source name (filename or identifier) */
  source_name: string;
}

export interface ParseResponse {
  /** Success status of the parsing operation */
  success: boolean;
  
  /** Human-readable message about the parsing result */
  message: string;
  
  /** Analysis identifier */
  analysis_id: string;
  
  /** Timestamp of the parsing operation */
  timestamp: string;
  
  /** Parsed data including biomarkers and metadata */
  parsed_data: {
    /** Metadata about the parsing operation */
    metadata: ParseMetadata;
    
    /** Array of extracted biomarkers */
    biomarkers: ParsedBiomarker[];
    
    /** Raw extracted text (for debugging/reference) */
    extracted_text: string;
  };
}

export interface ValidationResponse {
  /** Whether the format is valid */
  valid: boolean;
  
  /** Detected file format or content type */
  detected_format: string;
  
  /** File size in bytes */
  file_size_bytes: number;
  
  /** List of supported formats */
  supported_formats: string[];
  
  /** Validation message */
  message: string;
}

export interface UploadError {
  /** Error code */
  code: string;
  
  /** Human-readable error message */
  message: string;
  
  /** Additional error details */
  details?: Record<string, any>;
}

export interface UploadState {
  /** Current upload/parsing status */
  status: "idle" | "uploading" | "parsing" | "ready" | "confirmed" | "error";
  
  /** Parsed biomarkers data */
  parsedData: ParsedBiomarker[];
  
  /** Current error state */
  error: UploadError | null;
  
  /** Analysis ID from last successful parse */
  analysisId: string | null;
  
  /** Source metadata */
  sourceMetadata: ParseMetadata | null;
}

export interface ParsingOptions {
  /** Maximum file size in bytes */
  maxFileSize?: number;
  
  /** Accepted file types */
  acceptedTypes?: string[];
  
  /** Whether to auto-confirm parsed results */
  autoConfirm?: boolean;
  
  /** Custom validation rules */
  validationRules?: {
    minBiomarkers?: number;
    maxBiomarkers?: number;
    requiredBiomarkers?: string[];
  };
}

// Hook return types for TanStack Query
export interface UseParseUploadResult {
  data: ParseResponse | undefined;
  error: Error | null;
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  mutate: (variables: { file?: File; text?: string }) => void;
  reset: () => void;
}

export interface UseValidateParsedResult {
  data: ValidationResponse | undefined;
  error: Error | null;
  isLoading: boolean;
  isSuccess: boolean;
  isError: boolean;
  mutate: (variables: { file?: File; text?: string }) => void;
  reset: () => void;
}
