"""
Cross-industry detector module for PrecisionTakeAI.

This module provides functionality to detect and classify elements from different industries
in PDF drawings and CAD files, including plumbing, electrical, structural, mechanical, and HVAC.
"""

import os
import numpy as np
from ..pdf_analysis.config import CROSS_INDUSTRY_CONFIG

class CrossIndustryDetector:
    """
    Detects and classifies elements from different industries in PDF drawings and CAD files.
    
    Features:
    - Multi-industry element detection
    - Configurable detection thresholds
    - Classification by industry type
    - Clash detection between elements
    - Confidence scoring
    """
    
    def __init__(self, config=None):
        """
        Initialize the cross-industry detector with configuration settings.
        
        Args:
            config (dict, optional): Configuration dictionary. If None, uses default config.
        """
        self.config = config or CROSS_INDUSTRY_CONFIG
        self.enabled_industries = self.config.get("industries", [])
        self.detection_threshold = self.config.get("detection_threshold", 0.75)
        self.mode = self.config.get("mode", "balanced")
        
        # Adjust parameters based on mode
        if self.mode == "performance":
            self.detection_threshold = max(0.85, self.detection_threshold)
            # Focus only on plumbing if in performance mode
            if "plumbing" in self.enabled_industries:
                self.enabled_industries = ["plumbing"]
        elif self.mode == "accuracy":
            self.detection_threshold = min(0.65, self.detection_threshold)
    
    def detect_elements(self, file_path):
        """
        Detect elements from different industries in the provided file.
        
        Args:
            file_path (str): Path to the PDF or CAD file
            
        Returns:
            dict: Dictionary containing detected elements by industry
        """
        # In a real implementation, this would use computer vision and ML models
        # For now, we'll simulate detection with random data
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Determine if this is a PDF or CAD file
        is_cad = file_extension in ['.dwg', '.dxf', '.stl', '.stp', '.step', '.dgn']
        is_pdf = file_extension == '.pdf'
        
        if not (is_cad or is_pdf):
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Simulate detection results
        results = {
            "file_info": {
                "filename": os.path.basename(file_path),
                "file_type": "CAD" if is_cad else "PDF",
                "format": file_extension[1:].upper()
            },
            "industries": {},
            "clashes": [],
            "metadata": {
                "detection_mode": self.mode,
                "detection_threshold": self.detection_threshold,
                "enabled_industries": self.enabled_industries
            }
        }
        
        # Generate simulated elements for each enabled industry
        for industry in self.enabled_industries:
            # Base element count varies by industry
            if industry == "plumbing":
                base_count = np.random.randint(30, 100)
            elif industry == "electrical":
                base_count = np.random.randint(20, 80)
            elif industry == "structural":
                base_count = np.random.randint(10, 40)
            elif industry == "mechanical":
                base_count = np.random.randint(5, 30)
            elif industry == "hvac":
                base_count = np.random.randint(5, 25)
            else:
                base_count = np.random.randint(5, 20)
            
            # Adjust count based on file type (CAD files typically have more elements)
            element_count = base_count * (1.5 if is_cad else 1.0)
            
            # Generate elements
            elements = []
            for i in range(int(element_count)):
                element = {
                    "id": f"{industry}-{i+1}",
                    "type": self._get_element_type(industry),
                    "position": {
                        "x": round(np.random.uniform(0, 1000), 2),
                        "y": round(np.random.uniform(0, 800), 2),
                        "z": round(np.random.uniform(0, 200), 2) if is_cad else 0
                    },
                    "confidence": round(np.random.uniform(self.detection_threshold, 0.99), 2)
                }
                
                # Add industry-specific properties
                if industry == "plumbing":
                    element["diameter"] = np.random.choice([0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0])
                    element["material"] = np.random.choice(["PVC", "Copper", "PEX", "Cast Iron", "Galvanized"])
                elif industry == "electrical":
                    element["voltage"] = np.random.choice([120, 240, 277, 480])
                    element["circuit"] = f"C-{np.random.randint(1, 50)}"
                
                elements.append(element)
            
            # Add to results
            results["industries"][industry] = {
                "element_count": len(elements),
                "elements": elements,
                "confidence_score": round(np.random.uniform(0.85, 0.98), 2)
            }
        
        # Generate clash detection results
        if len(self.enabled_industries) > 1:
            clash_count = np.random.randint(0, 10)
            for i in range(clash_count):
                # Select two random industries
                industries = np.random.choice(self.enabled_industries, 2, replace=False)
                
                # Create a clash between elements from these industries
                clash = {
                    "id": f"clash-{i+1}",
                    "type": np.random.choice(["hard_clash", "clearance_issue"]),
                    "severity": np.random.choice(["critical", "major", "minor"]),
                    "elements": [
                        f"{industries[0]}-{np.random.randint(1, results['industries'][industries[0]]['element_count'])}",
                        f"{industries[1]}-{np.random.randint(1, results['industries'][industries[1]]['element_count'])}"
                    ],
                    "position": {
                        "x": round(np.random.uniform(0, 1000), 2),
                        "y": round(np.random.uniform(0, 800), 2),
                        "z": round(np.random.uniform(0, 200), 2) if is_cad else 0
                    }
                }
                results["clashes"].append(clash)
        
        return results
    
    def filter_by_industry(self, detection_results, industries=None):
        """
        Filter detection results to include only specified industries.
        
        Args:
            detection_results (dict): Results from detect_elements
            industries (list, optional): List of industries to include. If None, uses all enabled industries.
            
        Returns:
            dict: Filtered detection results
        """
        if industries is None:
            return detection_results
        
        filtered_results = detection_results.copy()
        filtered_industries = {}
        
        for industry in industries:
            if industry in detection_results["industries"]:
                filtered_industries[industry] = detection_results["industries"][industry]
        
        filtered_results["industries"] = filtered_industries
        
        # Filter clashes to only include elements from filtered industries
        if "clashes" in filtered_results:
            filtered_clashes = []
            for clash in filtered_results["clashes"]:
                element_industries = [element.split("-")[0] for element in clash["elements"]]
                if all(industry in industries for industry in element_industries):
                    filtered_clashes.append(clash)
            filtered_results["clashes"] = filtered_clashes
        
        return filtered_results
    
    def detect_clashes(self, detection_results):
        """
        Detect clashes between elements from different industries.
        
        Args:
            detection_results (dict): Results from detect_elements
            
        Returns:
            list: List of detected clashes
        """
        # In a real implementation, this would analyze element positions and dimensions
        # For now, we'll return the simulated clashes from detect_elements
        return detection_results.get("clashes", [])
    
    def _get_element_type(self, industry):
        """
        Get a random element type for the specified industry.
        
        Args:
            industry (str): Industry name
            
        Returns:
            str: Element type
        """
        if industry == "plumbing":
            return np.random.choice([
                "pipe", "elbow", "tee", "valve", "sink", "toilet", "shower", "water_heater"
            ])
        elif industry == "electrical":
            return np.random.choice([
                "conduit", "junction_box", "outlet", "switch", "panel", "light_fixture"
            ])
        elif industry == "structural":
            return np.random.choice([
                "beam", "column", "wall", "footing", "slab", "joist"
            ])
        elif industry == "mechanical":
            return np.random.choice([
                "duct", "damper", "fan", "unit", "diffuser", "grille"
            ])
        elif industry == "hvac":
            return np.random.choice([
                "duct", "diffuser", "grille", "unit", "thermostat", "damper"
            ])
        else:
            return "unknown"
