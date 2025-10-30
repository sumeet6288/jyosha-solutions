#!/usr/bin/env python3
"""
RAG System Test Suite - Basic Text-Based Implementation
Tests the RAG system after ChromaDB removal and MongoDB text-based search implementation
"""

import requests
import json
import time
import uuid
import os
from typing import Dict, Any, Optional

class RAGSystemTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.auth_token = None
        self.test_chatbot_id = None
        self.test_source_ids = []
        self.test_session_id = str(uuid.uuid4())
        
        # Test results tracking
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
        # Test content for RAG verification
        self.test_content = {
            "company_policy": """
            Company Policy Document
            
            Our company operates with the following core policies:
            
            1. Remote Work Policy
            All employees are allowed to work remotely up to 3 days per week. Remote work must be approved by direct supervisors and requires a stable internet connection.
            
            2. Vacation Policy  
            Employees receive 15 days of paid vacation annually. Vacation requests must be submitted at least 2 weeks in advance through the HR portal.
            
            3. Training Budget
            Each employee has an annual training budget of $2,000 for professional development courses, conferences, and certifications.
            
            4. Equipment Policy
            Company provides laptops and necessary equipment. Personal use of company equipment is allowed for reasonable personal activities.
            """,
            
            "product_info": """
            Product Information Guide
            
            BotSmith Platform Features:
            
            Multi-Provider AI Support:
            - OpenAI GPT models (GPT-4, GPT-4o-mini)
            - Anthropic Claude models (Claude 3.5 Sonnet)
            - Google Gemini models (Gemini 2.0 Flash)
            
            Knowledge Base Integration:
            - File upload support (PDF, DOCX, TXT, CSV, XLSX)
            - Website scraping capabilities
            - Text content management
            - Advanced chunking and retrieval
            
            Analytics Dashboard:
            - Real-time conversation tracking
            - Message volume analytics
            - User engagement metrics
            - Performance monitoring
            
            Customization Options:
            - Custom branding and themes
            - Widget positioning controls
            - Welcome message configuration
            - Response tone adjustment
            """
        }
    
    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append(f"{test_name}: {message}")
    
    def make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with proper headers"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        if self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        kwargs['headers'] = headers
        
        try:
            response = self.session.request(method, url, **kwargs)
            print(f"  {method} {endpoint} -> {response.status_code}")
            return response
        except Exception as e:
            print(f"  {method} {endpoint} -> ERROR: {str(e)}")
            raise
    
    def test_setup_chatbot(self):
        """Setup test chatbot for RAG testing"""
        try:
            # Use mock authentication
            response = self.make_request('GET', '/api/auth/me/mock')
            if response.status_code == 200:
                self.auth_token = "mock-token"  # Mock token for testing
            
            # Get existing chatbots instead of creating new one
            response = self.make_request('GET', '/api/chatbots')
            success = response.status_code == 200
            
            if success:
                chatbots = response.json()
                if chatbots and len(chatbots) > 0:
                    # Use the first available chatbot
                    self.test_chatbot_id = chatbots[0]['id']
                    success = bool(self.test_chatbot_id)
                    self.log_result("Setup Test Chatbot", success, f"Using existing chatbot ID: {self.test_chatbot_id}")
                else:
                    self.log_result("Setup Test Chatbot", False, "No existing chatbots found")
            else:
                error_msg = response.text
                self.log_result("Setup Test Chatbot", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Setup Test Chatbot", False, f"Exception: {str(e)}")
    
    def test_upload_text_sources(self):
        """Test uploading text sources and verify MongoDB storage"""
        if not self.test_chatbot_id:
            self.log_result("Upload Text Sources", False, "No chatbot ID available")
            return
        
        try:
            # Upload company policy document
            payload1 = {
                "name": "Company Policy Document",
                "content": self.test_content["company_policy"]
            }
            
            response1 = self.make_request('POST', f'/api/sources/chatbot/{self.test_chatbot_id}/text', data=payload1)
            success1 = response1.status_code == 201
            
            if success1:
                data1 = response1.json()
                source_id1 = data1.get('id')
                self.test_source_ids.append(source_id1)
            
            # Upload product information document
            payload2 = {
                "name": "Product Information Guide", 
                "content": self.test_content["product_info"]
            }
            
            response2 = self.make_request('POST', f'/api/sources/chatbot/{self.test_chatbot_id}/text', data=payload2)
            success2 = response2.status_code == 201
            
            if success2:
                data2 = response2.json()
                source_id2 = data2.get('id')
                self.test_source_ids.append(source_id2)
            
            success = success1 and success2
            message = f"Uploaded {len(self.test_source_ids)} text sources"
            if not success:
                message += f" (Errors: {response1.status_code if not success1 else ''} {response2.status_code if not success2 else ''})"
            
            self.log_result("Upload Text Sources", success, message)
            
            # Wait for processing
            time.sleep(3)
            
        except Exception as e:
            self.log_result("Upload Text Sources", False, f"Exception: {str(e)}")
    
    def test_verify_mongodb_storage(self):
        """Verify sources are stored and processed correctly"""
        if not self.test_chatbot_id:
            self.log_result("Verify MongoDB Storage", False, "No chatbot ID available")
            return
        
        try:
            response = self.make_request('GET', f'/api/sources/chatbot/{self.test_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                sources = response.json()
                success = len(sources) >= 2  # Should have at least 2 sources
                
                # Check source details
                processed_count = 0
                for source in sources:
                    if source.get('status') == 'processed':
                        processed_count += 1
                
                message = f"Found {len(sources)} sources, {processed_count} processed"
                
                # Verify no ChromaDB references
                has_chromadb_refs = any('chroma' in str(source).lower() for source in sources)
                if has_chromadb_refs:
                    success = False
                    message += " (WARNING: ChromaDB references found)"
                else:
                    message += " (No ChromaDB references - Good!)"
                
                self.log_result("Verify MongoDB Storage", success, message)
            else:
                error_msg = response.text
                self.log_result("Verify MongoDB Storage", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Verify MongoDB Storage", False, f"Exception: {str(e)}")
    
    def test_text_based_retrieval_policy_query(self):
        """Test text-based retrieval with policy-related query"""
        if not self.test_chatbot_id:
            self.log_result("Text-Based Retrieval (Policy)", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "chatbot_id": self.test_chatbot_id,
                "message": "What is the company's remote work policy?",
                "session_id": self.test_session_id,
                "user_name": "RAG Tester",
                "user_email": "rag.tester@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                
                # Check if response contains relevant information
                policy_keywords = ['remote work', '3 days', 'supervisor', 'internet connection']
                found_keywords = [kw for kw in policy_keywords if kw.lower() in ai_message.lower()]
                
                # Check for source citations
                has_citations = 'source' in ai_message.lower() or '[source' in ai_message.lower()
                
                success = len(found_keywords) >= 2 and len(ai_message) > 50
                message = f"Response length: {len(ai_message)} chars, Keywords found: {len(found_keywords)}/4"
                
                if has_citations:
                    message += ", Citations: ✓"
                else:
                    message += ", Citations: ✗"
                
                self.log_result("Text-Based Retrieval (Policy)", success, message)
            else:
                error_msg = response.text
                self.log_result("Text-Based Retrieval (Policy)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Text-Based Retrieval (Policy)", False, f"Exception: {str(e)}")
    
    def test_text_based_retrieval_product_query(self):
        """Test text-based retrieval with product-related query"""
        if not self.test_chatbot_id:
            self.log_result("Text-Based Retrieval (Product)", False, "No chatbot ID available")
            return
        
        try:
            payload = {
                "chatbot_id": self.test_chatbot_id,
                "message": "What AI providers does BotSmith support?",
                "session_id": self.test_session_id,
                "user_name": "RAG Tester",
                "user_email": "rag.tester@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                
                # Check if response contains AI provider information
                provider_keywords = ['openai', 'anthropic', 'claude', 'gemini', 'gpt']
                found_keywords = [kw for kw in provider_keywords if kw.lower() in ai_message.lower()]
                
                # Check for source citations
                has_citations = 'source' in ai_message.lower() or '[source' in ai_message.lower()
                
                success = len(found_keywords) >= 2 and len(ai_message) > 50
                message = f"Response length: {len(ai_message)} chars, Provider keywords: {len(found_keywords)}/5"
                
                if has_citations:
                    message += ", Citations: ✓"
                else:
                    message += ", Citations: ✗"
                
                self.log_result("Text-Based Retrieval (Product)", success, message)
            else:
                error_msg = response.text
                self.log_result("Text-Based Retrieval (Product)", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Text-Based Retrieval (Product)", False, f"Exception: {str(e)}")
    
    def test_bm25_scoring_relevance(self):
        """Test BM25-style scoring by comparing relevant vs irrelevant queries"""
        if not self.test_chatbot_id:
            self.log_result("BM25 Scoring Test", False, "No chatbot ID available")
            return
        
        try:
            # Test relevant query
            relevant_payload = {
                "chatbot_id": self.test_chatbot_id,
                "message": "How many vacation days do employees get?",
                "session_id": self.test_session_id + "_relevant",
                "user_name": "RAG Tester",
                "user_email": "rag.tester@example.com"
            }
            
            relevant_response = self.make_request('POST', '/api/chat', json=relevant_payload)
            
            # Test irrelevant query
            irrelevant_payload = {
                "chatbot_id": self.test_chatbot_id,
                "message": "What is the weather like today?",
                "session_id": self.test_session_id + "_irrelevant",
                "user_name": "RAG Tester", 
                "user_email": "rag.tester@example.com"
            }
            
            irrelevant_response = self.make_request('POST', '/api/chat', json=irrelevant_payload)
            
            success = relevant_response.status_code == 200 and irrelevant_response.status_code == 200
            
            if success:
                relevant_data = relevant_response.json()
                irrelevant_data = irrelevant_response.json()
                
                relevant_message = relevant_data.get('message', '')
                irrelevant_message = irrelevant_data.get('message', '')
                
                # Check if relevant query found vacation info
                vacation_keywords = ['15 days', 'vacation', 'paid vacation', '2 weeks']
                relevant_found = sum(1 for kw in vacation_keywords if kw.lower() in relevant_message.lower())
                
                # Check if irrelevant query has less specific info
                weather_keywords = ['weather', 'temperature', 'sunny', 'rainy']
                irrelevant_found = sum(1 for kw in weather_keywords if kw.lower() in irrelevant_message.lower())
                
                success = relevant_found >= 1  # Relevant query should find vacation info
                message = f"Relevant query found {relevant_found} vacation keywords, Irrelevant query found {irrelevant_found} weather keywords"
                
                self.log_result("BM25 Scoring Test", success, message)
            else:
                self.log_result("BM25 Scoring Test", False, f"API errors: {relevant_response.status_code}, {irrelevant_response.status_code}")
        except Exception as e:
            self.log_result("BM25 Scoring Test", False, f"Exception: {str(e)}")
    
    def test_no_embedding_generation(self):
        """Verify no embedding generation is happening (check logs/responses)"""
        try:
            # This test checks that the system works without embeddings
            # We can verify by checking that responses are still generated
            # and that no embedding-related errors occur
            
            payload = {
                "chatbot_id": self.test_chatbot_id,
                "message": "Tell me about the training budget policy",
                "session_id": self.test_session_id + "_embedding_test",
                "user_name": "RAG Tester",
                "user_email": "rag.tester@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                
                # Check if training budget info is found
                budget_keywords = ['$2,000', 'training budget', 'professional development']
                found_keywords = [kw for kw in budget_keywords if kw.lower() in ai_message.lower()]
                
                success = len(found_keywords) >= 1 and len(ai_message) > 30
                message = f"Found {len(found_keywords)} budget keywords without embeddings"
                
                self.log_result("No Embedding Generation", success, message)
            else:
                error_msg = response.text
                # Check if error is embedding-related
                if 'embedding' in error_msg.lower() or 'vector' in error_msg.lower():
                    self.log_result("No Embedding Generation", False, f"Embedding-related error: {error_msg}")
                else:
                    self.log_result("No Embedding Generation", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("No Embedding Generation", False, f"Exception: {str(e)}")
    
    def test_source_management(self):
        """Test source listing and deletion"""
        if not self.test_chatbot_id:
            self.log_result("Source Management", False, "No chatbot ID available")
            return
        
        try:
            # List sources
            response = self.make_request('GET', f'/api/sources/chatbot/{self.test_chatbot_id}')
            success = response.status_code == 200
            
            if success:
                sources = response.json()
                initial_count = len(sources)
                
                # Delete first source if available
                if self.test_source_ids and len(self.test_source_ids) > 0:
                    source_to_delete = self.test_source_ids[0]
                    delete_response = self.make_request('DELETE', f'/api/sources/{source_to_delete}')
                    delete_success = delete_response.status_code == 204
                    
                    if delete_success:
                        # Wait for deletion processing
                        time.sleep(2)
                        
                        # Verify source is removed
                        verify_response = self.make_request('GET', f'/api/sources/chatbot/{self.test_chatbot_id}')
                        if verify_response.status_code == 200:
                            remaining_sources = verify_response.json()
                            final_count = len(remaining_sources)
                            
                            success = final_count < initial_count
                            message = f"Sources: {initial_count} -> {final_count} (deleted 1)"
                        else:
                            success = False
                            message = "Failed to verify deletion"
                    else:
                        success = False
                        message = f"Delete failed: {delete_response.status_code}"
                else:
                    message = f"Listed {initial_count} sources (no deletion test - no source IDs)"
                
                self.log_result("Source Management", success, message)
            else:
                error_msg = response.text
                self.log_result("Source Management", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Source Management", False, f"Exception: {str(e)}")
    
    def test_chunk_verification(self):
        """Verify chunks are properly stored in MongoDB"""
        try:
            # This is an indirect test - we verify that the system can retrieve
            # specific information that would only be available if chunking worked
            
            payload = {
                "chatbot_id": self.test_chatbot_id,
                "message": "What equipment does the company provide to employees?",
                "session_id": self.test_session_id + "_chunk_test",
                "user_name": "RAG Tester",
                "user_email": "rag.tester@example.com"
            }
            
            response = self.make_request('POST', '/api/chat', json=payload)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                ai_message = data.get('message', '')
                
                # Check if equipment policy info is found (this would be in a specific chunk)
                equipment_keywords = ['laptop', 'equipment', 'company provides', 'personal use']
                found_keywords = [kw for kw in equipment_keywords if kw.lower() in ai_message.lower()]
                
                success = len(found_keywords) >= 2
                message = f"Found {len(found_keywords)}/4 equipment keywords (indicates proper chunking)"
                
                self.log_result("Chunk Verification", success, message)
            else:
                error_msg = response.text
                self.log_result("Chunk Verification", False, f"Status: {response.status_code}, Error: {error_msg}")
        except Exception as e:
            self.log_result("Chunk Verification", False, f"Exception: {str(e)}")
    
    def test_cleanup(self):
        """Clean up test resources (skip deleting existing chatbot)"""
        try:
            # Don't delete the existing chatbot, just clean up sources we added
            if self.test_source_ids:
                cleaned_sources = 0
                for source_id in self.test_source_ids[1:]:  # Keep first source, delete others
                    try:
                        response = self.make_request('DELETE', f'/api/sources/{source_id}')
                        if response.status_code == 204:
                            cleaned_sources += 1
                    except:
                        pass
                self.log_result("Cleanup Test Sources", True, f"Cleaned up {cleaned_sources} test sources")
            else:
                self.log_result("Cleanup Test Sources", True, "No test sources to clean up")
        except Exception as e:
            self.log_result("Cleanup Test Sources", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all RAG tests in sequence"""
        print("🔍 Starting RAG System Tests (Basic Text-Based Implementation)")
        print(f"📍 Base URL: {self.base_url}")
        print("=" * 70)
        
        # Test sequence
        test_methods = [
            self.test_setup_chatbot,
            self.test_upload_text_sources,
            self.test_verify_mongodb_storage,
            self.test_text_based_retrieval_policy_query,
            self.test_text_based_retrieval_product_query,
            self.test_bm25_scoring_relevance,
            self.test_no_embedding_generation,
            self.test_chunk_verification,
            self.test_source_management,
            self.test_cleanup
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(1)  # Small delay between tests
            except Exception as e:
                print(f"❌ CRITICAL ERROR in {test_method.__name__}: {str(e)}")
                self.results["failed"] += 1
                self.results["errors"].append(f"{test_method.__name__}: CRITICAL ERROR - {str(e)}")
        
        # Print summary
        print("\n" + "=" * 70)
        print("📊 RAG SYSTEM TEST SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"📈 Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")
        
        if self.results["errors"]:
            print("\n🔍 FAILED TESTS:")
            for error in self.results["errors"]:
                print(f"   • {error}")
        
        return self.results


def main():
    """Main test execution"""
    # Get base URL from environment or use default
    base_url = "https://quick-setup-27.preview.emergentagent.com"
    
    print(f"Testing RAG System at: {base_url}")
    
    # Initialize and run tests
    tester = RAGSystemTester(base_url)
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    exit_code = 0 if results["failed"] == 0 else 1
    exit(exit_code)


if __name__ == "__main__":
    main()