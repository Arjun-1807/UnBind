import os
import time
from typing import List, Dict, Any
from groq import Groq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
import chromadb
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.groq_client = Groq(api_key=settings.GROQ_API_KEY)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_db = None
        
    def process_document(self, text: str, document_id: str) -> Dict[str, Any]:
        """Process document text and create vector embeddings"""
        start_time = time.time()
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create documents for vector store
        documents = [Document(page_content=chunk, metadata={"document_id": document_id}) for chunk in chunks]
        
        # Create or update vector store
        if self.vector_db is None:
            self.vector_db = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=f"document_{document_id}"
            )
        else:
            self.vector_db.add_documents(documents)
        
        # Generate analysis using GROQ
        analysis = self._generate_analysis(text, chunks)
        
        processing_time = int(time.time() - start_time)
        
        return {
            "analysis": analysis,
            "processing_time": processing_time,
            "chunks_count": len(chunks),
            "confidence_score": 85  # Placeholder
        }
    
    def _generate_analysis(self, full_text: str, chunks: List[str]) -> str:
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
        
        Make the explanation clear and accessible to non-lawyers.
        """
        
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
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
        """Query documents using similarity search"""
        if self.vector_db is None:
            return []
        
        # Perform similarity search
        results = self.vector_db.similarity_search_with_score(query, k=5)
        
        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": float(score)
            })
        
        return formatted_results
