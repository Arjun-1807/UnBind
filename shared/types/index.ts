// User types
export interface User {
  id: number
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at?: string
}

export interface UserCreate {
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface UserUpdate {
  first_name?: string
  last_name?: string
}

// Document types
export interface Document {
  id: number
  user_id: number
  filename: string
  original_filename: string
  file_path: string
  file_size: number
  mime_type: string
  status: 'uploaded' | 'processing' | 'analyzed' | 'error'
  created_at: string
  updated_at?: string
}

export interface DocumentCreate {
  filename: string
}

// Analysis types
export interface Analysis {
  id: number
  document_id: number
  analysis_type: string
  original_text?: string
  simplified_text: string
  analysis_data?: Record<string, any>
  confidence_score?: number
  processing_time?: number
  created_at: string
}

export interface AnalysisCreate {
  document_id: number
  analysis_type: string
  simplified_text: string
  original_text?: string
  analysis_data?: Record<string, any>
  confidence_score?: number
}

// Authentication types
export interface LoginRequest {
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export interface TokenData {
  email?: string
}

// API Response types
export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

// File types
export interface FileUpload {
  file: File
  status: 'uploading' | 'success' | 'error'
  progress: number
  error?: string
}

// Common types
export interface PaginationParams {
  page?: number
  size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface SearchParams extends PaginationParams {
  query?: string
  filters?: Record<string, any>
}
