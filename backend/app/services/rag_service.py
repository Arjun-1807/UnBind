import os
import time
from typing import List, Dict, Any
from groq import Groq
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        self.documents_store = {}  # Simple in-memory storage
        
    def process_document(self, text: str, document_id: str) -> Dict[str, Any]:
        """Process document text and create simplified analysis"""
        start_time = time.time()
        
        # Store document text (simple storage)
        self.documents_store[document_id] = text
        
        # Generate analysis using GROQ
        analysis = self._generate_analysis(text)
        
        processing_time = int(time.time() - start_time)
        
        return {
            "analysis": analysis,
            "processing_time": processing_time,
            "chunks_count": 1,  # Simplified
            "confidence_score": 85
        }
    
    def _generate_analysis(self, full_text: str) -> str:
        """Generate simplified analysis using GROQ"""
        
        prompt = f"""
        You are a legal document expert. Analyze the following legal document and provide a simple, easy-to-understand explanation.
        
        Document text:
        {full_text[:4000]}  # Limit text length for API
        
        Please provide:
        1. A simple summary in plain English
        2. Key points and obligations
        3. Any potential risks or concerns
        4. Recommendations for the reader
        5. Mention the risk level(in percentage)
        6. Also mention key dates
        Make the explanation clear and accessible to non-lawyers.
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Standard available model
                messages=[
                    {"role": "system", "content": "You are a helpful legal document analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Analysis failed: {str(e)}"
    
    def query_documents(self, query: str, document_ids: List[str] = None) -> List[Dict[str, Any]]:
        """Simple query using stored documents"""
        if not self.documents_store:
            return []
        
        # Simple text search (not vector similarity)
        results = []
        for doc_id, text in self.documents_store.items():
            if document_ids and doc_id not in document_ids:
                continue
                
            # Simple keyword matching
            if query.lower() in text.lower():
                results.append({
                    "content": text[:200] + "...",  # Truncate for display
                    "metadata": {"document_id": doc_id},
                    "similarity_score": 0.8  # Placeholder
                })
        
        return results[:5]  # Limit results
