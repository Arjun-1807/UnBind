'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { useDropzone } from 'react-dropzone'
import { FileText, Upload, X, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'

interface UploadedFile {
  id: string
  file: File
  status: 'uploading' | 'success' | 'error'
  progress: number
  error?: string
}

export default function UploadPage() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const router = useRouter()

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles: UploadedFile[] = acceptedFiles.map(file => ({
      id: Math.random().toString(36).substr(2, 9),
      file,
      status: 'uploading',
      progress: 0
    }))

    setUploadedFiles(prev => [...prev, ...newFiles])
    handleUpload(newFiles)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'text/plain': ['.txt']
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: true
  })

  const handleUpload = async (files: UploadedFile[]) => {
    setIsUploading(true)

    for (const fileData of files) {
      try {
        const formData = new FormData()
        formData.append('file', fileData.file)

        const token = localStorage.getItem('token')
        if (!token) {
          router.push('/auth/login')
          return
        }

        const response = await fetch('/api/v1/documents/upload', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`
          },
          body: formData
        })

        if (response.ok) {
          setUploadedFiles(prev => 
            prev.map(f => 
              f.id === fileData.id 
                ? { ...f, status: 'success', progress: 100 }
                : f
            )
          )
          toast.success(`${fileData.file.name} uploaded successfully!`)
        } else {
          const error = await response.json()
          setUploadedFiles(prev => 
            prev.map(f => 
              f.id === fileData.id 
                ? { ...f, status: 'error', error: error.detail || 'Upload failed' }
                : f
            )
          )
          toast.error(`${fileData.file.name} upload failed`)
        }
      } catch (error) {
        setUploadedFiles(prev => 
          prev.map(f => 
            f.id === fileData.id 
              ? { ...f, status: 'error', error: 'Network error' }
              : f
          )
        )
        toast.error(`${fileData.file.name} upload failed`)
      }
    }

    setIsUploading(false)
  }

  const removeFile = (id: string) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== id))
  }

  const retryUpload = (fileData: UploadedFile) => {
    setUploadedFiles(prev => 
      prev.map(f => 
        f.id === fileData.id 
          ? { ...f, status: 'uploading', progress: 0, error: undefined }
          : f
      )
    )
    handleUpload([fileData])
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">UnBind</span>
            </div>
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/dashboard')}
                className="text-gray-600 hover:text-gray-900"
              >
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Upload Documents</h1>
          <p className="text-gray-600 mt-2">
            Upload your legal documents for AI-powered analysis and simplification
          </p>
        </div>

        {/* Upload Area */}
        <div className="card mb-8">
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-primary-400 bg-primary-50'
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }`}
          >
            <input {...getInputProps()} />
            <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            {isDragActive ? (
              <p className="text-lg text-primary-600">Drop the files here...</p>
            ) : (
              <div>
                <p className="text-lg text-gray-900 mb-2">
                  Drag & drop files here, or click to select
                </p>
                <p className="text-sm text-gray-500">
                  Supports PDF, DOCX, DOC, and TXT files up to 10MB
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Uploaded Files */}
        {uploadedFiles.length > 0 && (
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Uploaded Files</h2>
            <div className="space-y-4">
              {uploadedFiles.map((fileData) => (
                <div
                  key={fileData.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex items-center space-x-4">
                    <FileText className="h-8 w-8 text-gray-400" />
                    <div>
                      <p className="font-medium text-gray-900">{fileData.file.name}</p>
                      <p className="text-sm text-gray-500">
                        {formatFileSize(fileData.file.size)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4">
                    {fileData.status === 'uploading' && (
                      <div className="flex items-center space-x-2">
                        <Loader2 className="h-4 w-4 animate-spin text-primary-600" />
                        <span className="text-sm text-gray-600">Uploading...</span>
                      </div>
                    )}

                    {fileData.status === 'success' && (
                      <div className="flex items-center space-x-2 text-green-600">
                        <CheckCircle className="h-5 w-5" />
                        <span className="text-sm">Uploaded</span>
                      </div>
                    )}

                    {fileData.status === 'error' && (
                      <div className="flex items-center space-x-2 text-red-600">
                        <AlertCircle className="h-5 w-5" />
                        <span className="text-sm">{fileData.error}</span>
                        <button
                          onClick={() => retryUpload(fileData)}
                          className="text-sm text-primary-600 hover:text-primary-700 underline"
                        >
                          Retry
                        </button>
                      </div>
                    )}

                    <button
                      onClick={() => removeFile(fileData.id)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {uploadedFiles.some(f => f.status === 'success') && (
              <div className="mt-6 text-center">
                <button
                  onClick={() => router.push('/dashboard')}
                  className="btn-primary"
                >
                  View Documents
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
