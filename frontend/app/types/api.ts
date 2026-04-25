// TODO: Define API types
export interface ApiResponse<T = unknown> {
  /** Present when `success` is true; may be null on failure (check `success` first). */
  data: T | null;
  success: boolean;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T = any> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface ApiError {
  message: string;
  code: string;
  details?: any;
}
