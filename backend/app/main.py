from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import uvicorn
import os
import PyPDF2
import random
import json
from datetime import datetime

# Import PDF analysis modules
from app.pdf_analysis.cross_industry_detector import CrossIndustryDetector
from app.pdf_analysis.ai_training import AITrainingPipeline
from app.pdf_analysis.global_compliance import GlobalComplianceFramework
from app.pdf_analysis.cad_converter import CADConverter
from app.pdf_analysis.performance_optimizer import PerformanceOptimizer
from app.pdf_analysis.config import CROSS_INDUSTRY_CONFIG, COMPLIANCE_CONFIG

# Initialize components
cross_industry_detector = CrossIndustryDetector()
ai_training_pipeline = AITrainingPipeline()
global_compliance_framework = GlobalComplianceFramework()
cad_converter = CADConverter()
performance_optimizer = PerformanceOptimizer()

app = FastAPI(title="PrecisionTake.ai API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# PDF upload endpoint (original version for backward compatibility)
@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        # Check if file is a PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process the PDF (basic analysis for now)
        analysis_result = analyze_pdf(file_path)
        
        return JSONResponse(content=analysis_result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Enhanced PDF analysis endpoint
@app.post("/api/analyze-pdf")
async def analyze_pdf_enhanced(
    file: UploadFile = File(...),
    detect_cross_industry: bool = Form(True),
    industries: List[str] = Form(["plumbing", "electrical", "structural", "mechanical", "hvac"]),
    check_compliance: bool = Form(True),
    regions: List[str] = Form(["australia", "global"]),
    mode: str = Form("balanced")  # Options: "performance", "accuracy", "balanced"
):
    try:
        # Check if file is a PDF or CAD file
        file_extension = os.path.splitext(file.filename.lower())[1]
        is_pdf = file_extension == '.pdf'
        is_cad = file_extension in ['.dwg', '.dxf', '.stl', '.stp', '.step', '.dgn']
        
        if not (is_pdf or is_cad):
            raise HTTPException(status_code=400, detail="File must be a PDF or supported CAD format")
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Convert CAD file to DXF if needed
        if is_cad and file_extension != '.dxf':
            conversion_result = cad_converter.convert(file_path)
            if conversion_result["status"] == "success":
                file_path = conversion_result["output_file"]
                print(f"Converted CAD file to: {file_path}")
        
        # Use cache to check if we've analyzed this file before
        cache_key = f"analysis_{os.path.basename(file_path)}_{mode}"
        cached_result, found = performance_optimizer.get_from_cache(cache_key)
        
        if found:
            print(f"Using cached analysis result for {file_path}")
            return JSONResponse(content=cached_result)
        
        # Process the file with enhanced analysis
        result = {}
        
        # Basic file info
        result["file_info"] = {
            "filename": os.path.basename(file_path),
            "file_type": "CAD" if is_cad else "PDF",
            "size_kb": os.path.getsize(file_path) / 1024
        }
        
        # Add PDF-specific info if it's a PDF
        if is_pdf:
            with open(file_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                result["file_info"]["pages"] = len(pdf_reader.pages)
        
        # Detect cross-industry elements if requested
        if detect_cross_industry:
            # Configure detector with requested mode and industries
            detector_config = CROSS_INDUSTRY_CONFIG.copy()
            detector_config["mode"] = mode
            detector_config["industries"] = [ind for ind in industries if ind in detector_config["industries"]]
            
            # Create detector with custom config
            detector = CrossIndustryDetector(detector_config)
            
            # Detect elements
            detection_results = detector.detect_elements(file_path)
            result["cross_industry"] = detection_results
            
            # Check compliance if requested
            if check_compliance and "plumbing" in detection_results["industries"]:
                compliance_results = global_compliance_framework.check_compliance(
                    detection_results, 
                    regions=[r for r in regions if r in global_compliance_framework.get_enabled_regions()]
                )
                result["compliance"] = compliance_results
        else:
            # Fall back to basic analysis for backward compatibility
            basic_analysis = analyze_pdf(file_path)
            result["symbols"] = basic_analysis["symbols"]
        
        # Add analysis metadata
        result["analysis_metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "industries_analyzed": industries if detect_cross_industry else ["plumbing"],
            "compliance_regions": regions if check_compliance else [],
            "model_version": ai_training_pipeline.get_model_info()["current_version"]
        }
        
        # Cache the result for future use
        performance_optimizer.put_in_cache(cache_key, result)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error in enhanced analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Cross-industry detection endpoint
@app.post("/api/detect-cross-industry")
async def detect_cross_industry(
    file: UploadFile = File(...),
    industries: List[str] = Form(["plumbing", "electrical", "structural", "mechanical", "hvac"]),
    mode: str = Form("balanced")  # Options: "performance", "accuracy", "balanced"
):
    try:
        # Check if file is a PDF or CAD file
        file_extension = os.path.splitext(file.filename.lower())[1]
        is_pdf = file_extension == '.pdf'
        is_cad = file_extension in ['.dwg', '.dxf', '.stl', '.stp', '.step', '.dgn']
        
        if not (is_pdf or is_cad):
            raise HTTPException(status_code=400, detail="File must be a PDF or supported CAD format")
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Configure detector with requested mode and industries
        detector_config = CROSS_INDUSTRY_CONFIG.copy()
        detector_config["mode"] = mode
        detector_config["industries"] = [ind for ind in industries if ind in detector_config["industries"]]
        
        # Create detector with custom config
        detector = CrossIndustryDetector(detector_config)
        
        # Detect elements
        detection_results = detector.detect_elements(file_path)
        
        return JSONResponse(content=detection_results)
    
    except Exception as e:
        print(f"Error in cross-industry detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Compliance checking endpoint
@app.post("/api/check-compliance")
async def check_compliance(
    file: UploadFile = File(...),
    regions: List[str] = Form(["australia", "global"])
):
    try:
        # Check if file is a PDF or CAD file
        file_extension = os.path.splitext(file.filename.lower())[1]
        is_pdf = file_extension == '.pdf'
        is_cad = file_extension in ['.dwg', '.dxf', '.stl', '.stp', '.step', '.dgn']
        
        if not (is_pdf or is_cad):
            raise HTTPException(status_code=400, detail="File must be a PDF or supported CAD format")
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # First detect elements with cross-industry detector
        detector = CrossIndustryDetector()
        detection_results = detector.detect_elements(file_path)
        
        # Then check compliance
        compliance_results = global_compliance_framework.check_compliance(
            detection_results, 
            regions=[r for r in regions if r in global_compliance_framework.get_enabled_regions()]
        )
        
        return JSONResponse(content=compliance_results)
    
    except Exception as e:
        print(f"Error in compliance checking: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# CAD conversion endpoint
@app.post("/api/convert-cad")
async def convert_cad(
    file: UploadFile = File(...),
    target_format: str = Form("DXF")
):
    try:
        # Check if file is a supported CAD format
        file_extension = os.path.splitext(file.filename.lower())[1][1:]  # Remove the dot
        if file_extension.upper() not in cad_converter.supported_formats:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported format: {file_extension}. Supported formats: {', '.join(cad_converter.supported_formats)}"
            )
        
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Convert the file
        conversion_result = cad_converter.convert(file_path)
        
        return JSONResponse(content=conversion_result)
    
    except Exception as e:
        print(f"Error in CAD conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# AI training feedback endpoint
@app.post("/api/feedback")
async def submit_feedback(
    file_id: str = Form(...),
    element_id: str = Form(...),
    original_detection: dict = Body(...),
    corrected_data: dict = Body(...),
    feedback_type: str = Form(...)  # Options: "element_correction", "clash_correction", etc.
):
    try:
        # Prepare feedback data
        feedback_data = {
            "file_id": file_id,
            "element_id": element_id,
            "original_detection": original_detection,
            "corrected_data": corrected_data,
            "feedback_type": feedback_type
        }
        
        # Submit feedback
        result = ai_training_pipeline.collect_feedback(feedback_data)
        
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error submitting feedback: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get model info endpoint
@app.get("/api/model-info")
async def get_model_info():
    try:
        model_info = ai_training_pipeline.get_model_info()
        return JSONResponse(content=model_info)
    
    except Exception as e:
        print(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Retrain model endpoint (admin only)
@app.post("/api/retrain-model")
async def retrain_model():
    try:
        result = ai_training_pipeline.retrain_model()
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error retraining model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get available compliance regions endpoint
@app.get("/api/compliance-regions")
async def get_compliance_regions():
    try:
        regions = global_compliance_framework.get_enabled_regions()
        region_standards = {
            region: global_compliance_framework.get_region_standards(region)
            for region in regions
        }
        
        return JSONResponse(content={
            "enabled_regions": regions,
            "region_standards": region_standards
        })
    
    except Exception as e:
        print(f"Error getting compliance regions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Get performance metrics endpoint
@app.get("/api/performance-metrics")
async def get_performance_metrics():
    try:
        metrics = performance_optimizer.get_performance_metrics()
        return JSONResponse(content=metrics)
    
    except Exception as e:
        print(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Clear cache endpoint (admin only)
@app.post("/api/clear-cache")
async def clear_cache():
    try:
        result = performance_optimizer.clear_cache()
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"Error clearing cache: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def analyze_pdf(file_path):
    """
    Analyze the PDF file and extract relevant information.
    This is a simplified version that will be enhanced with actual CV/ML later.
    """
    try:
        # Open the PDF file
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get basic information
            num_pages = len(pdf_reader.pages)
            
            # Extract text from first page (for basic analysis)
            first_page = pdf_reader.pages[0]
            text = first_page.extract_text()
            
            # Generate simulated analysis results
            # In a real implementation, this would use computer vision and ML
            
            # Determine complexity based on page count
            complexity_factor = min(num_pages * 0.5, 1.0)
            
            # Simulate symbol detection
            symbol_count = int(random.uniform(20, 100) * complexity_factor)
            
            # Simulate pipe length calculation
            total_pipe_length = random.uniform(100, 500) * complexity_factor
            
            # Generate materials list
            materials = [
                {"type": "PVC Pipe (2\")", "quantity": f"{int(total_pipe_length * 0.4)} ft"},
                {"type": "Copper Pipe (3/4\")", "quantity": f"{int(total_pipe_length * 0.3)} ft"},
                {"type": "Elbows (2\")", "quantity": f"{int(symbol_count * 0.15)} pcs"},
                {"type": "T-Joints (2\")", "quantity": f"{int(symbol_count * 0.12)} pcs"},
                {"type": "Valves (Ball)", "quantity": f"{int(symbol_count * 0.08)} pcs"},
                {"type": "Fixtures (Sink)", "quantity": f"{int(symbol_count * 0.05)} pcs"},
                {"type": "Fixtures (Toilet)", "quantity": f"{int(symbol_count * 0.03)} pcs"}
            ]
            
            # Calculate confidence score (simulated)
            confidence_score = 95 + random.uniform(0, 4.9)
            
            # Return analysis results
            return {
                "file_info": {
                    "filename": os.path.basename(file_path),
                    "pages": num_pages,
                    "size_kb": os.path.getsize(file_path) / 1024
                },
                "symbols": {
                    "count": symbol_count,
                    "total_pipe_length": total_pipe_length,
                    "materials": materials,
                    "confidence_score": round(confidence_score, 1)
                },
                "analysis_time": f"{random.uniform(1.5, 5.0):.1f} seconds"
            }
    
    except Exception as e:
        print(f"Error analyzing PDF: {str(e)}")
        return {
            "error": str(e),
            "file": os.path.basename(file_path)
        }

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
