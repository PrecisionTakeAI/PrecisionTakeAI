"""
Global compliance framework module for PrecisionTakeAI.

This module provides functionality to check compliance with plumbing codes
and standards from different regions around the world.
"""

import os
import json
import datetime
from ..pdf_analysis.config import COMPLIANCE_CONFIG

class GlobalComplianceFramework:
    """
    Checks compliance with plumbing codes and standards from different regions.
    
    Features:
    - Multi-region compliance checking
    - Detailed compliance reports
    - Severity classification
    - Recommendations for addressing issues
    """
    
    def __init__(self, config=None):
        """
        Initialize the global compliance framework with configuration settings.
        
        Args:
            config (dict, optional): Configuration dictionary. If None, uses default config.
        """
        self.config = config or COMPLIANCE_CONFIG
        self.regions = self.config.get("regions", {})
        self.severity_levels = self.config.get("severity_levels", ["critical", "major", "minor"])
        
        # Load compliance rules for each enabled region
        self.rules = self._load_compliance_rules()
    
    def _load_compliance_rules(self):
        """
        Load compliance rules for each enabled region.
        
        In a real implementation, this would load rules from a database or files.
        For now, we'll use hardcoded rules for demonstration.
        
        Returns:
            dict: Compliance rules by region
        """
        rules = {}
        
        # Australia rules (AS/NZS 3500)
        australia_rules = [
            {
                "id": "aus-001",
                "standard": "AS/NZS 3500",
                "description": "Minimum pipe size for water supply",
                "requirement": "Water supply pipes must be at least 15mm in diameter",
                "severity": "major",
                "check_function": lambda element: element.get("diameter", 0) >= 0.5,  # 0.5 inches ≈ 15mm
                "recommendation": "Increase pipe diameter to at least 15mm (0.5 inches)"
            },
            {
                "id": "aus-002",
                "standard": "AS/NZS 3500",
                "description": "Minimum fall for drainage pipes",
                "requirement": "Drainage pipes must have a minimum fall of 1:60",
                "severity": "major",
                "check_function": lambda element: True,  # Simplified for simulation
                "recommendation": "Adjust pipe slope to at least 1:60"
            },
            {
                "id": "aus-003",
                "standard": "AS/NZS 3500",
                "description": "Backflow prevention",
                "requirement": "Backflow prevention devices must be installed where required",
                "severity": "critical",
                "check_function": lambda element: True,  # Simplified for simulation
                "recommendation": "Install appropriate backflow prevention device"
            }
        ]
        
        # USA rules (UPC/IPC)
        usa_rules = [
            {
                "id": "usa-001",
                "standard": "UPC",
                "description": "Minimum pipe size for water supply",
                "requirement": "Water supply pipes must be at least 1/2 inch in diameter",
                "severity": "major",
                "check_function": lambda element: element.get("diameter", 0) >= 0.5,
                "recommendation": "Increase pipe diameter to at least 1/2 inch"
            },
            {
                "id": "usa-002",
                "standard": "IPC",
                "description": "Minimum slope for drainage pipes",
                "requirement": "Drainage pipes must have a minimum slope of 1/4 inch per foot",
                "severity": "major",
                "check_function": lambda element: True,  # Simplified for simulation
                "recommendation": "Adjust pipe slope to at least 1/4 inch per foot"
            }
        ]
        
        # UK rules (BS EN 806, BS EN 12056)
        uk_rules = [
            {
                "id": "uk-001",
                "standard": "BS EN 806",
                "description": "Minimum pipe size for water supply",
                "requirement": "Water supply pipes must be at least 15mm in diameter",
                "severity": "major",
                "check_function": lambda element: element.get("diameter", 0) >= 0.5,  # 0.5 inches ≈ 15mm
                "recommendation": "Increase pipe diameter to at least 15mm"
            }
        ]
        
        # EU rules (EN 806, EN 12056)
        eu_rules = [
            {
                "id": "eu-001",
                "standard": "EN 806",
                "description": "Minimum pipe size for water supply",
                "requirement": "Water supply pipes must be at least 15mm in diameter",
                "severity": "major",
                "check_function": lambda element: element.get("diameter", 0) >= 0.5,  # 0.5 inches ≈ 15mm
                "recommendation": "Increase pipe diameter to at least 15mm"
            }
        ]
        
        # Canada rules (NPC)
        canada_rules = [
            {
                "id": "can-001",
                "standard": "NPC",
                "description": "Minimum pipe size for water supply",
                "requirement": "Water supply pipes must be at least 1/2 inch in diameter",
                "severity": "major",
                "check_function": lambda element: element.get("diameter", 0) >= 0.5,
                "recommendation": "Increase pipe diameter to at least 1/2 inch"
            }
        ]
        
        # Global rules (ISO standards)
        global_rules = [
            {
                "id": "global-001",
                "standard": "ISO 15874",
                "description": "PP pipe material requirements",
                "requirement": "PP pipes must comply with ISO 15874 specifications",
                "severity": "major",
                "check_function": lambda element: element.get("material", "") != "PP" or True,  # Only check PP pipes
                "recommendation": "Ensure PP pipes comply with ISO 15874 specifications"
            }
        ]
        
        # Add rules for enabled regions
        for region, config in self.regions.items():
            if config.get("enabled", False):
                if region == "australia":
                    rules["australia"] = australia_rules
                elif region == "usa":
                    rules["usa"] = usa_rules
                elif region == "uk":
                    rules["uk"] = uk_rules
                elif region == "eu":
                    rules["eu"] = eu_rules
                elif region == "canada":
                    rules["canada"] = canada_rules
                elif region == "global":
                    rules["global"] = global_rules
        
        return rules
    
    def check_compliance(self, detection_results, regions=None):
        """
        Check compliance with plumbing codes and standards from specified regions.
        
        Args:
            detection_results (dict): Results from cross-industry detection
            regions (list, optional): List of regions to check. If None, checks all enabled regions.
            
        Returns:
            dict: Compliance check results
        """
        if regions is None:
            regions = [region for region, config in self.regions.items() if config.get("enabled", False)]
        else:
            # Filter to only include enabled regions
            regions = [region for region in regions if region in self.regions and self.regions[region].get("enabled", False)]
        
        if not regions:
            return {"status": "error", "message": "No enabled regions specified for compliance check"}
        
        # Get plumbing elements from detection results
        plumbing_elements = []
        if "industries" in detection_results and "plumbing" in detection_results["industries"]:
            plumbing_elements = detection_results["industries"]["plumbing"].get("elements", [])
        
        if not plumbing_elements:
            return {
                "status": "warning",
                "message": "No plumbing elements found for compliance check",
                "regions_checked": regions,
                "compliance_issues": [],
                "compliance_score": 100
            }
        
        # Check compliance for each region
        compliance_issues = []
        for region in regions:
            if region not in self.rules:
                continue
            
            region_rules = self.rules[region]
            for rule in region_rules:
                # Check each plumbing element against this rule
                for element in plumbing_elements:
                    try:
                        if not rule["check_function"](element):
                            # Rule violation found
                            issue = {
                                "rule_id": rule["id"],
                                "region": region,
                                "standard": rule["standard"],
                                "description": rule["description"],
                                "requirement": rule["requirement"],
                                "severity": rule["severity"],
                                "element_id": element["id"],
                                "element_type": element["type"],
                                "recommendation": rule["recommendation"]
                            }
                            compliance_issues.append(issue)
                    except Exception as e:
                        # Skip this check if there's an error
                        continue
        
        # Calculate compliance score
        total_checks = len(plumbing_elements) * sum(len(self.rules.get(region, [])) for region in regions)
        if total_checks == 0:
            compliance_score = 100
        else:
            # Weight by severity
            severity_weights = {"critical": 10, "major": 5, "minor": 1}
            weighted_issues = sum(severity_weights.get(issue["severity"], 1) for issue in compliance_issues)
            compliance_score = max(0, 100 - (weighted_issues * 100 / total_checks))
        
        return {
            "status": "success",
            "regions_checked": regions,
            "compliance_issues": compliance_issues,
            "compliance_score": round(compliance_score, 1),
            "timestamp": datetime.datetime.now().isoformat(),
            "issue_count": {
                "total": len(compliance_issues),
                "by_severity": {
                    severity: len([i for i in compliance_issues if i["severity"] == severity])
                    for severity in self.severity_levels
                },
                "by_region": {
                    region: len([i for i in compliance_issues if i["region"] == region])
                    for region in regions
                }
            }
        }
    
    def get_enabled_regions(self):
        """
        Get list of enabled regions for compliance checking.
        
        Returns:
            list: Enabled regions
        """
        return [region for region, config in self.regions.items() if config.get("enabled", False)]
    
    def get_region_standards(self, region):
        """
        Get list of standards for a specific region.
        
        Args:
            region (str): Region name
            
        Returns:
            list: Standards for the specified region
        """
        if region in self.regions:
            return self.regions[region].get("standards", [])
        return []
