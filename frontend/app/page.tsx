'use client'

import Link from 'next/link'
import { ArrowRight, FileText, Shield, Zap, Users } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white/80 backdrop-blur-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <FileText className="h-8 w-8 text-primary-600" />
              <span className="ml-2 text-xl font-bold text-gray-900">UnBind</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/auth/login" className="text-gray-600 hover:text-gray-900">
                Login
              </Link>
              <Link href="/auth/signup" className="btn-primary">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Understand Legal Documents
            <span className="text-primary-600"> Instantly</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload your legal documents and get AI-powered analysis that breaks down complex legal language into simple, easy-to-understand explanations.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/auth/signup" className="btn-primary text-lg px-8 py-3">
              Start Analyzing
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
            <Link href="/auth/login" className="btn-secondary text-lg px-8 py-3">
              Sign In
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Why Choose UnBind?
          </h2>
          <p className="text-lg text-gray-600">
            Powerful AI technology that makes legal documents accessible to everyone
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="card text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Fast Analysis</h3>
            <p className="text-gray-600">
              Get instant analysis of your legal documents using advanced AI and RAG technology
            </p>
          </div>

          <div className="card text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Secure & Private</h3>
            <p className="text-gray-600">
              Your documents are processed securely and never shared with third parties
            </p>
          </div>

          <div className="card text-center">
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Users className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Easy to Use</h3>
            <p className="text-gray-600">
              Simple, intuitive interface designed for both legal professionals and individuals
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Simplify Your Legal Documents?
          </h2>
          <p className="text-primary-100 mb-8 text-lg">
            Join thousands of users who trust UnBind for their legal document analysis needs
          </p>
          <Link href="/auth/signup" className="bg-white text-primary-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg text-lg transition-colors duration-200">
            Get Started Free
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <FileText className="h-8 w-8 text-primary-400" />
              <span className="ml-2 text-xl font-bold">UnBind</span>
            </div>
            <p className="text-gray-400">
              © 2024 UnBind. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
