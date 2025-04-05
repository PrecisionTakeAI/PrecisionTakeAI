"""
Configuration settings for the PDF analysis module.

This module contains configuration parameters for:
- Cross-industry detection
- AI training pipeline
- Global compliance framework
- CAD conversion
- Performance optimization
"""

# General configuration
DEBUG = True
UPLOAD_FOLDER = "uploads"
RESULTS_FOLDER = "results"

# Cross-industry detection configuration
CROSS_INDUSTRY_CONFIG = {
    "enabled": True,
    "industries": ["plumbing", "electrical", "structural", "mechanical", "hvac"],
    "detection_threshold": 0.75,  # Confidence threshold for detection
    "mode": "balanced",  # Options: "performance", "accuracy", "balanced"
}

# AI training pipeline configuration
AI_TRAINING_CONFIG = {
    "collect_feedback": True,
    "feedback_storage": "feedback_data",
    "auto_retrain": False,
    "training_interval_days": 7,
    "min_feedback_samples": 50,
}

# Global compliance framework configuration
COMPLIANCE_CONFIG = {
    "regions": {
        "australia": {
            "enabled": True,
            "standards": ["AS/NZS 3500"],
        },
        "usa": {
            "enabled": False,
            "standards": ["UPC", "IPC"],
        },
        "uk": {
            "enabled": False,
            "standards": ["BS EN 806", "BS EN 12056"],
        },
        "eu": {
            "enabled": False,
            "standards": ["EN 806", "EN 12056"],
        },
        "canada": {
            "enabled": False,
            "standards": ["NPC"],
        },
        "global": {
            "enabled": True,
            "standards": ["ISO 15874", "ISO 15875"],
        }
    },
    "severity_levels": ["critical", "major", "minor"],
}

# CAD conversion configuration
CAD_CONVERSION_CONFIG = {
    "supported_formats": ["DWG", "DXF", "STL", "STP", "STEP", "DGN"],
    "target_format": "DXF",
    "preserve_metadata": True,
    "conversion_quality": "high",  # Options: "low", "medium", "high"
}

# Performance optimization configuration
PERFORMANCE_CONFIG = {
    "caching": {
        "enabled": True,
        "memory_cache_size_mb": 100,
        "disk_cache_size_mb": 500,
        "ttl_seconds": 3600,
    },
    "parallel_processing": {
        "enabled": True,
        "max_workers": 4,  # Set to 0 to use CPU count
        "use_processes": True,  # False for threads, True for processes
    },
    "resource_monitoring": {
        "enabled": True,
        "max_memory_percent": 80,
        "max_cpu_percent": 90,
    }
}
