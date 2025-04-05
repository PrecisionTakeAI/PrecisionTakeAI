"""
System test script for PrecisionTakeAI integrated components.

This script tests the integrated FastAPI application with all enhanced components:
- Cross-industry detector
- AI training pipeline
- Global compliance framework
- CAD converter
- Performance optimizer
"""

import os
import sys
import time
import json
import requests
from datetime import datetime

# Test configuration
API_URL = "http://localhost:8000"
TEST_PDF_FILE = "../uploads/Plumbing Drawings.pdf"
TEST_RESULTS_DIR = "test_results"

def create_test_cad_file():
    """Create a test CAD file for testing."""
    test_file = "test_drawing.dwg"
    with open(test_file, "w") as f:
        f.write("Mock CAD file content")
    return test_file

def test_health_endpoint():
    """Test the health endpoint."""
    print("\n=== Testing Health Endpoint ===")
    
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        result = response.json()
        
        print(f"Status: {result['status']}")
        print(f"Timestamp: {result['timestamp']}")
        
        return True, result
    except Exception as e:
        print(f"Error testing health endpoint: {str(e)}")
        return False, None

def test_original_pdf_upload():
    """Test the original PDF upload endpoint for backward compatibility."""
    print("\n=== Testing Original PDF Upload Endpoint ===")
    
    if not os.path.exists(TEST_PDF_FILE):
        print(f"Test PDF file not found: {TEST_PDF_FILE}")
        return False, None
    
    try:
        with open(TEST_PDF_FILE, "rb") as f:
            files = {"file": (os.path.basename(TEST_PDF_FILE), f, "application/pdf")}
            response = requests.post(f"{API_URL}/api/upload-pdf", files=files)
            response.raise_for_status()
            result = response.json()
        
        print(f"File: {result['file_info']['filename']}")
        print(f"Pages: {result['file_info']['pages']}")
        print(f"Symbols detected: {result['symbols']['count']}")
        print(f"Pipe length: {result['symbols']['total_pipe_length']:.1f} ft")
        print(f"Confidence score: {result['symbols']['confidence_score']}%")
        
        return True, result
    except Exception as e:
        print(f"Error testing original PDF upload: {str(e)}")
        return False, None

def test_enhanced_pdf_analysis():
    """Test the enhanced PDF analysis endpoint."""
    print("\n=== Testing Enhanced PDF Analysis Endpoint ===")
    
    if not os.path.exists(TEST_PDF_FILE):
        print(f"Test PDF file not found: {TEST_PDF_FILE}")
        return False, None
    
    try:
        with open(TEST_PDF_FILE, "rb") as f:
            files = {"file": (os.path.basename(TEST_PDF_FILE), f, "application/pdf")}
            data = {
                "detect_cross_industry": "true",
                "industries": ["plumbing", "electrical", "structural"],
                "check_compliance": "true",
                "regions": ["australia", "global"],
                "mode": "balanced"
            }
            response = requests.post(f"{API_URL}/api/analyze-pdf", files=files, data=data)
            response.raise_for_status()
            result = response.json()
        
        print(f"File: {result['file_info']['filename']}")
        print(f"File type: {result['file_info']['file_type']}")
        
        if "cross_industry" in result:
            industries = result["cross_industry"]["industries"]
            print(f"Industries detected: {len(industries)}")
            for industry, data in industries.items():
                print(f"  - {industry}: {data['element_count']} elements")
            
            if "clashes" in result["cross_industry"]:
                print(f"Clashes detected: {len(result['cross_industry']['clashes'])}")
        
        if "compliance" in result:
            print(f"Compliance score: {result['compliance']['compliance_score']}")
            print(f"Compliance issues: {result['compliance']['issue_count']['total']}")
        
        print(f"Model version: {result['analysis_metadata']['model_version']}")
        
        return True, result
    except Exception as e:
        print(f"Error testing enhanced PDF analysis: {str(e)}")
        return False, None

def test_cross_industry_detection():
    """Test the cross-industry detection endpoint."""
    print("\n=== Testing Cross-Industry Detection Endpoint ===")
    
    if not os.path.exists(TEST_PDF_FILE):
        print(f"Test PDF file not found: {TEST_PDF_FILE}")
        return False, None
    
    try:
        with open(TEST_PDF_FILE, "rb") as f:
            files = {"file": (os.path.basename(TEST_PDF_FILE), f, "application/pdf")}
            data = {
                "industries": ["plumbing", "electrical", "structural"],
                "mode": "accuracy"
            }
            response = requests.post(f"{API_URL}/api/detect-cross-industry", files=files, data=data)
            response.raise_for_status()
            result = response.json()
        
        print(f"File: {result['file_info']['filename']}")
        
        industries = result["industries"]
        print(f"Industries detected: {len(industries)}")
        for industry, data in industries.items():
            print(f"  - {industry}: {data['element_count']} elements, confidence: {data['confidence_score']}")
        
        if "clashes" in result:
            print(f"Clashes detected: {len(result['clashes'])}")
        
        return True, result
    except Exception as e:
        print(f"Error testing cross-industry detection: {str(e)}")
        return False, None

def test_compliance_checking():
    """Test the compliance checking endpoint."""
    print("\n=== Testing Compliance Checking Endpoint ===")
    
    if not os.path.exists(TEST_PDF_FILE):
        print(f"Test PDF file not found: {TEST_PDF_FILE}")
        return False, None
    
    try:
        with open(TEST_PDF_FILE, "rb") as f:
            files = {"file": (os.path.basename(TEST_PDF_FILE), f, "application/pdf")}
            data = {
                "regions": ["australia", "global"]
            }
            response = requests.post(f"{API_URL}/api/check-compliance", files=files, data=data)
            response.raise_for_status()
            result = response.json()
        
        print(f"Status: {result['status']}")
        print(f"Regions checked: {result['regions_checked']}")
        print(f"Compliance score: {result['compliance_score']}")
        print(f"Compliance issues: {result['issue_count']['total']}")
        
        for severity, count in result['issue_count']['by_severity'].items():
            if count > 0:
                print(f"  - {severity}: {count} issues")
        
        return True, result
    except Exception as e:
        print(f"Error testing compliance checking: {str(e)}")
        return False, None

def test_cad_conversion():
    """Test the CAD conversion endpoint."""
    print("\n=== Testing CAD Conversion Endpoint ===")
    
    # Create a test CAD file
    test_file = create_test_cad_file()
    
    try:
        with open(test_file, "rb") as f:
            files = {"file": (test_file, f, "application/octet-stream")}
            data = {
                "target_format": "DXF"
            }
            response = requests.post(f"{API_URL}/api/convert-cad", files=files, data=data)
            response.raise_for_status()
            result = response.json()
        
        print(f"Status: {result['status']}")
        print(f"Input file: {result['input_file']}")
        print(f"Output file: {result['output_file']}")
        print(f"Conversion type: {result['conversion_type']}")
        
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
        
        return True, result
    except Exception as e:
        print(f"Error testing CAD conversion: {str(e)}")
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)
        return False, None

def test_ai_feedback():
    """Test the AI feedback endpoint."""
    print("\n=== Testing AI Feedback Endpoint ===")
    
    try:
        data = {
            "file_id": "test_file_001",
            "element_id": "plumbing-42",
            "feedback_type": "element_correction"
        }
        
        json_data = {
            "original_detection": {
                "type": "pipe",
                "position": {"x": 100, "y": 200, "z": 0},
                "confidence": 0.85
            },
            "corrected_data": {
                "type": "valve",
                "position": {"x": 100, "y": 200, "z": 0}
            }
        }
        
        response = requests.post(f"{API_URL}/api/feedback", data=data, json=json_data)
        response.raise_for_status()
        result = response.json()
        
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        if "feedback_id" in result:
            print(f"Feedback ID: {result['feedback_id']}")
        
        return True, result
    except Exception as e:
        print(f"Error testing AI feedback: {str(e)}")
        return False, None

def test_model_info():
    """Test the model info endpoint."""
    print("\n=== Testing Model Info Endpoint ===")
    
    try:
        response = requests.get(f"{API_URL}/api/model-info")
        response.raise_for_status()
        result = response.json()
        
        print(f"Current version: {result['current_version']}")
        print(f"Accuracy: {result['performance_metrics']['accuracy']}")
        print(f"Precision: {result['performance_metrics']['precision']}")
        print(f"Recall: {result['performance_metrics']['recall']}")
        
        return True, result
    except Exception as e:
        print(f"Error testing model info: {str(e)}")
        return False, None

def test_compliance_regions():
    """Test the compliance regions endpoint."""
    print("\n=== Testing Compliance Regions Endpoint ===")
    
    try:
        response = requests.get(f"{API_URL}/api/compliance-regions")
        response.raise_for_status()
        result = response.json()
        
        print(f"Enabled regions: {result['enabled_regions']}")
        for region, standards in result['region_standards'].items():
            print(f"  - {region}: {', '.join(standards)}")
        
        return True, result
    except Exception as e:
        print(f"Error testing compliance regions: {str(e)}")
        return False, None

def test_performance_metrics():
    """Test the performance metrics endpoint."""
    print("\n=== Testing Performance Metrics Endpoint ===")
    
    try:
        response = requests.get(f"{API_URL}/api/performance-metrics")
        response.raise_for_status()
        result = response.json()
        
        print(f"Cache hits: {result['cache_hits']}")
        print(f"Cache misses: {result['cache_misses']}")
        print(f"Parallel tasks completed: {result['parallel_tasks_completed']}")
        print(f"Average task time: {result['average_task_time_ms']:.2f} ms")
        
        print(f"Memory usage: {result['current_resource_usage']['memory_percent']}%")
        print(f"CPU usage: {result['current_resource_usage']['cpu_percent']}%")
        
        return True, result
    except Exception as e:
        print(f"Error testing performance metrics: {str(e)}")
        return False, None

def run_all_tests():
    """Run all system tests and generate a report."""
    print("\n=== PrecisionTakeAI System Tests ===")
    print(f"Started at: {datetime.now().isoformat()}")
    print(f"API URL: {API_URL}")
    
    # Create test results directory
    os.makedirs(TEST_RESULTS_DIR, exist_ok=True)
    
    test_results = {}
    
    # Run tests
    test_results["health_endpoint"] = test_health_endpoint()
    test_results["original_pdf_upload"] = test_original_pdf_upload()
    test_results["enhanced_pdf_analysis"] = test_enhanced_pdf_analysis()
    test_results["cross_industry_detection"] = test_cross_industry_detection()
    test_results["compliance_checking"] = test_compliance_checking()
    test_results["cad_conversion"] = test_cad_conversion()
    test_results["ai_feedback"] = test_ai_feedback()
    test_results["model_info"] = test_model_info()
    test_results["compliance_regions"] = test_compliance_regions()
    test_results["performance_metrics"] = test_performance_metrics()
    
    # Generate summary
    print("\n=== Test Summary ===")
    all_passed = True
    for endpoint, (passed, _) in test_results.items():
        status = "PASSED" if passed else "FAILED"
        if not passed:
            all_passed = False
        print(f"{endpoint}: {status}")
    
    overall_status = "PASSED" if all_passed else "FAILED"
    print(f"\nOverall test status: {overall_status}")
    
    # Save test results to file
    results_file = os.path.join(TEST_RESULTS_DIR, f"system_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "endpoint_status": {endpoint: passed for endpoint, (passed, _) in test_results.items()}
        }, f, indent=2)
    
    print(f"Test results saved to: {results_file}")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
