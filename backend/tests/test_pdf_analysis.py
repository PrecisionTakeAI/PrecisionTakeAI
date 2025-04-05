"""
Test script for PrecisionTakeAI PDF analysis module.

This script tests the functionality of the PDF analysis module components:
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
from datetime import datetime

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules to test
from app.pdf_analysis.cross_industry_detector import CrossIndustryDetector
from app.pdf_analysis.ai_training import AITrainingPipeline
from app.pdf_analysis.global_compliance import GlobalComplianceFramework
from app.pdf_analysis.cad_converter import CADConverter
from app.pdf_analysis.performance_optimizer import PerformanceOptimizer

def test_cross_industry_detector():
    """Test the cross-industry detector functionality."""
    print("\n=== Testing Cross-Industry Detector ===")
    
    # Initialize detector
    detector = CrossIndustryDetector()
    print(f"Initialized detector with mode: {detector.mode}")
    print(f"Enabled industries: {detector.enabled_industries}")
    
    # Test with a sample PDF file
    sample_file = "../uploads/Plumbing Drawings.pdf"
    if os.path.exists(sample_file):
        print(f"Testing with sample file: {sample_file}")
        try:
            results = detector.detect_elements(sample_file)
            print(f"Detection successful. Found elements in {len(results['industries'])} industries")
            
            # Print summary of detected elements
            for industry, data in results['industries'].items():
                print(f"  - {industry}: {data['element_count']} elements, confidence: {data['confidence_score']}")
            
            # Print clash information
            print(f"Detected {len(results['clashes'])} potential clashes")
            
            return True, results
        except Exception as e:
            print(f"Error in detection: {str(e)}")
            return False, None
    else:
        print(f"Sample file not found: {sample_file}")
        # Create a mock file for testing
        mock_file = "test_plumbing.pdf"
        with open(mock_file, "w") as f:
            f.write("Test PDF content")
        
        print(f"Created mock file for testing: {mock_file}")
        try:
            results = detector.detect_elements(mock_file)
            print(f"Detection successful with mock file. Found elements in {len(results['industries'])} industries")
            
            # Clean up mock file
            os.remove(mock_file)
            return True, results
        except Exception as e:
            print(f"Error in detection with mock file: {str(e)}")
            # Clean up mock file
            if os.path.exists(mock_file):
                os.remove(mock_file)
            return False, None

def test_ai_training_pipeline():
    """Test the AI training pipeline functionality."""
    print("\n=== Testing AI Training Pipeline ===")
    
    # Initialize pipeline
    pipeline = AITrainingPipeline()
    print("Initialized AI training pipeline")
    
    # Get model info
    model_info = pipeline.get_model_info()
    print(f"Current model version: {model_info['current_version']}")
    print(f"Current accuracy: {model_info['performance_metrics']['accuracy']}")
    
    # Test feedback collection
    feedback_data = {
        "file_id": "test_file_001",
        "element_id": "plumbing-42",
        "original_detection": {
            "type": "pipe",
            "position": {"x": 100, "y": 200, "z": 0},
            "confidence": 0.85
        },
        "corrected_data": {
            "type": "valve",
            "position": {"x": 100, "y": 200, "z": 0}
        },
        "feedback_type": "element_correction"
    }
    
    try:
        result = pipeline.collect_feedback(feedback_data)
        print(f"Feedback collection result: {result['status']}")
        
        # Test model retraining
        retrain_result = pipeline.retrain_model()
        print(f"Model retraining result: {retrain_result['status']}")
        print(f"New model version: {retrain_result['new_version']}")
        print(f"Accuracy improvement: {retrain_result['improvement']['accuracy']}")
        
        # Get feedback stats
        stats = pipeline.get_feedback_stats()
        print(f"Total feedback collected: {stats['total_feedback']}")
        
        return True, {
            "model_info": model_info,
            "feedback_result": result,
            "retrain_result": retrain_result,
            "feedback_stats": stats
        }
    except Exception as e:
        print(f"Error in AI training pipeline: {str(e)}")
        return False, None

def test_global_compliance_framework():
    """Test the global compliance framework functionality."""
    print("\n=== Testing Global Compliance Framework ===")
    
    # Initialize framework
    framework = GlobalComplianceFramework()
    print("Initialized global compliance framework")
    
    # Get enabled regions
    enabled_regions = framework.get_enabled_regions()
    print(f"Enabled regions: {enabled_regions}")
    
    # Create mock detection results
    mock_results = {
        "industries": {
            "plumbing": {
                "element_count": 10,
                "elements": [
                    {
                        "id": "plumbing-1",
                        "type": "pipe",
                        "diameter": 0.25,  # Too small, should trigger compliance issue
                        "material": "PVC",
                        "position": {"x": 100, "y": 200, "z": 0},
                        "confidence": 0.9
                    },
                    {
                        "id": "plumbing-2",
                        "type": "pipe",
                        "diameter": 0.75,  # OK size
                        "material": "Copper",
                        "position": {"x": 300, "y": 400, "z": 0},
                        "confidence": 0.95
                    }
                ]
            }
        }
    }
    
    try:
        # Check compliance
        compliance_results = framework.check_compliance(mock_results)
        print(f"Compliance check status: {compliance_results['status']}")
        print(f"Compliance score: {compliance_results['compliance_score']}")
        print(f"Found {compliance_results['issue_count']['total']} compliance issues")
        
        # Print issues by severity
        for severity, count in compliance_results['issue_count']['by_severity'].items():
            if count > 0:
                print(f"  - {severity}: {count} issues")
        
        return True, compliance_results
    except Exception as e:
        print(f"Error in compliance framework: {str(e)}")
        return False, None

def test_cad_converter():
    """Test the CAD converter functionality."""
    print("\n=== Testing CAD Converter ===")
    
    # Initialize converter
    converter = CADConverter()
    print("Initialized CAD converter")
    print(f"Supported formats: {converter.supported_formats}")
    
    # Create a mock CAD file
    mock_file = "test_drawing.dwg"
    with open(mock_file, "w") as f:
        f.write("Mock CAD file content")
    
    try:
        # Test format detection
        is_supported = converter.is_supported_format(mock_file)
        print(f"Format detection: {'Supported' if is_supported else 'Not supported'}")
        
        # Test conversion
        if is_supported:
            result = converter.convert(mock_file)
            print(f"Conversion result: {result['status']}")
            print(f"Output file: {result['output_file']}")
            
            # Test metadata extraction
            metadata = converter.extract_metadata(mock_file)
            print(f"Metadata extraction: {metadata['status']}")
            if metadata['status'] == 'success':
                print(f"File type: {metadata['file_type']}")
                print(f"Format: {metadata['format']}")
        
        # Clean up
        if os.path.exists(mock_file):
            os.remove(mock_file)
        
        return True, {
            "is_supported": is_supported,
            "conversion_result": result if is_supported else None,
            "metadata": metadata if is_supported else None
        }
    except Exception as e:
        print(f"Error in CAD converter: {str(e)}")
        # Clean up
        if os.path.exists(mock_file):
            os.remove(mock_file)
        return False, None

def test_performance_optimizer():
    """Test the performance optimizer functionality."""
    print("\n=== Testing Performance Optimizer ===")
    
    # Initialize optimizer
    optimizer = PerformanceOptimizer()
    print("Initialized performance optimizer")
    
    try:
        # Test caching
        cache_key = "test_cache_key"
        cache_data = {"test": "data", "timestamp": datetime.now().isoformat()}
        
        # Put in cache
        cache_result = optimizer.put_in_cache(cache_key, cache_data)
        print(f"Cache put result: {'Success' if cache_result else 'Failed'}")
        
        # Get from cache
        cached_data, found = optimizer.get_from_cache(cache_key)
        print(f"Cache get result: {'Found' if found else 'Not found'}")
        
        # Test parallel processing
        def test_func(item):
            time.sleep(0.1)  # Simulate work
            return item * 2
        
        items = list(range(10))
        start_time = time.time()
        results = optimizer.run_in_parallel(test_func, items)
        end_time = time.time()
        
        print(f"Parallel processing completed in {end_time - start_time:.2f} seconds")
        print(f"Results: {results[:3]}... (showing first 3)")
        
        # Get performance metrics
        metrics = optimizer.get_performance_metrics()
        print(f"Cache hit ratio: {metrics['cache_statistics']['cache_hit_ratio']:.2f}")
        print(f"Average task time: {metrics['average_task_time_ms']:.2f} ms")
        print(f"Current CPU usage: {metrics['current_resource_usage']['cpu_percent']}%")
        print(f"Current memory usage: {metrics['current_resource_usage']['memory_percent']}%")
        
        # Test cache clearing
        clear_result = optimizer.clear_cache()
        print(f"Cache clear result: {clear_result['status']}")
        
        return True, {
            "cache_test": {"put": cache_result, "get": found},
            "parallel_test": {"time": end_time - start_time, "results": results},
            "performance_metrics": metrics,
            "clear_cache": clear_result
        }
    except Exception as e:
        print(f"Error in performance optimizer: {str(e)}")
        return False, None

def run_all_tests():
    """Run all tests and generate a report."""
    print("\n=== PrecisionTakeAI PDF Analysis Module Tests ===")
    print(f"Started at: {datetime.now().isoformat()}")
    
    test_results = {}
    
    # Run tests
    test_results["cross_industry_detector"] = test_cross_industry_detector()
    test_results["ai_training_pipeline"] = test_ai_training_pipeline()
    test_results["global_compliance_framework"] = test_global_compliance_framework()
    test_results["cad_converter"] = test_cad_converter()
    test_results["performance_optimizer"] = test_performance_optimizer()
    
    # Generate summary
    print("\n=== Test Summary ===")
    all_passed = True
    for module, (passed, _) in test_results.items():
        status = "PASSED" if passed else "FAILED"
        if not passed:
            all_passed = False
        print(f"{module}: {status}")
    
    overall_status = "PASSED" if all_passed else "FAILED"
    print(f"\nOverall test status: {overall_status}")
    
    # Save test results to file
    results_dir = "test_results"
    os.makedirs(results_dir, exist_ok=True)
    
    results_file = os.path.join(results_dir, f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "module_status": {module: passed for module, (passed, _) in test_results.items()}
        }, f, indent=2)
    
    print(f"Test results saved to: {results_file}")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
