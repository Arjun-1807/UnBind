#!/usr/bin/env python3
"""
Simple test script for RAG functionality
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.services.rag_service import RAGService

def test_rag():
    """Test basic RAG functionality"""
    
    # Check if GROQ API key is set
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set GROQ_API_KEY in your .env file")
        print(f"Looking for .env file at: {env_path}")
        return False
    
    print("✅ GROQ API key found")
    
    # Initialize RAG service
    try:
        rag_service = RAGService()
        print("✅ RAG service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RAG service: {e}")
        return False
    
    # Test document processing
    test_document = """
    Loan Agreement 
This Loan Agreement ("Agreement") dated 12-12-2023 is made and entered into as of this 3rd day of September, 
2025, by and between Apex Financial Solutions, a Delaware corporation ("Lender"), and 
John P. Doe, an individual residing at 123 Maple Street, Anytown, USA ("Borrower"). 
1. Loan Amount, Terms, and Repayment 
The Lender agrees to lend to the Borrower the principal sum of $50,000.00 ("Principal"). The 
loan shall bear a variable interest rate equal to the Lender's Prime Rate plus 5%, with the 
Prime Rate being defined as the rate of interest publicly announced by the Lender from time 
to time as its reference rate, and said rate may be adjusted by the Lender at its sole discretion 
without prior notification to the Borrower. The Borrower shall repay the Principal and all 
accrued interest in 60 equal monthly installments of $1,125.00, beginning on October 3, 2025. 
All payments are due on the 3rd of each month. Any payment received more than seven (7) 
days after the due date shall incur a late fee of $50.00, in addition to any other remedies 
available to the Lender. 
2. Prepayment and Acceleration due date 12-12-2026
The Borrower may make a full or partial prepayment of the Principal at any time, subject to a 
prepayment fee equal to the sum of (a) all interest that would have accrued through the 
remainder of the loan term, had the loan not been prepaid, and (b) an administrative fee of 
$1,000.00. Notwithstanding the foregoing, if the Lender, in its sole judgment, determines that 
a material adverse change has occurred in the Borrower’s financial condition or prospects, 
the Lender may, at its option, declare the entire outstanding Principal, together with all 
accrued and unpaid interest and fees, immediately due and payable without presentment, 
demand, protest, or other notice of any kind. 
3. Security and Covenants 
To secure the full and timely performance of all obligations under this Agreement, the 
Borrower hereby grants to the Lender a first-priority security interest in and to all of the 
Borrower's property, whether real or personal, tangible or intangible, now owned or hereafter 
acquired. This includes, but is not limited to, all bank accounts, investment portfolios, real 
estate holdings, motor vehicles, and any and all proceeds and products thereof. The Borrower 
covenants to maintain a debt-to-income ratio of no more than 35% throughout the term of 
this loan and to provide the Lender with copies of all personal and business financial 
statements, tax returns, and asset declarations within ten (10) days of the Lender's request. 
Failure to comply with any of these covenants shall constitute a default under this Agreement. 
4. Indemnification and Waiver 
The Borrower agrees to indemnify and hold harmless the Lender, its officers, agents, and 
employees from any and all claims, damages, liabilities, and expenses, including reasonable 
attorneys' fees, arising from or in connection with the Borrower's failure to perform any 
obligation under this Agreement. The Borrower expressly waives any and all rights and 
defenses against the Lender, including but not limited to the right to offset any amounts owed, 
or any right to a jury trial or to participate in any class action lawsuit. All disputes shall be 
subject to binding arbitration in a venue selected by the Lender. 
IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first written 
above. 
Lender: 
Apex Financial Solutions 
By: _________________________ 
Name: [Authorized Signatory Name] 
Title: [Title] 
Borrower: 
By: _________________________ 
Name: John P. Doe 
Date: _________________________
    """
    
    print("\n📄 Testing document processing...")
    try:
        result = rag_service.process_document(test_document, "test_doc_001")
        print("✅ Document processed successfully")
        print(f"⏱️  Processing time: {result['processing_time']} seconds")
        print(f"📊 Confidence score: {result['confidence_score']}%")
        print("\n📝 Analysis:")
        print("-" * 50)
        print(result['analysis'])
        print("-" * 50)
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        return False
    
    # Test document querying
    print("\n🔍 Testing document querying...")
    try:
        query_results = rag_service.query_documents("rent payment", ["test_doc_001"])
        print(f"✅ Query successful, found {len(query_results)} results")
        
        for i, result in enumerate(query_results, 1):
            print(f"\nResult {i}:")
            print(f"Content: {result['content']}")
            print(f"Document ID: {result['metadata']['document_id']}")
            print(f"Similarity Score: {result['similarity_score']}")
            
    except Exception as e:
        print(f"❌ Document querying failed: {e}")
        return False
    
    print("\n🎉 All RAG tests passed successfully!")
    return True

if __name__ == "__main__":
    print("🚀 Testing RAG (Retrieval-Augmented Generation) functionality...")
    print("=" * 60)
    
    success = test_rag()
    
    if success:
        print("\n✅ RAG system is working correctly!")
        print("You can now use this in your FastAPI application.")
    else:
        print("\n❌ RAG system test failed.")
        print("Please check the error messages above.")
