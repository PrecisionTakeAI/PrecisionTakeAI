"""
Performance optimization configuration for PrecisionTakeAI.

This module contains configuration settings for the performance optimizer.
"""

# Performance optimization configuration
PERFORMANCE_CONFIG = {
    # Caching configuration
    "caching": {
        "enabled": True,
        "memory_cache_size_mb": 200,  # Increased from 100MB to 200MB
        "disk_cache_size_mb": 1000,   # Increased from 500MB to 1GB
        "ttl_seconds": 7200           # Increased from 3600s (1h) to 7200s (2h)
    },
    
    # Parallel processing configuration
    "parallel_processing": {
        "enabled": True,
        "max_workers": 8,             # Optimized for typical server cores
        "use_processes": False        # Changed to threads for better memory sharing
    },
    
    # Resource monitoring configuration
    "resource_monitoring": {
        "enabled": True,
        "max_memory_percent": 85,     # Increased from 80% to 85%
        "max_cpu_percent": 90,
        "check_interval_seconds": 3   # Reduced from 5s to 3s for more responsive monitoring
    },
    
    # Adaptive optimization
    "adaptive_optimization": {
        "enabled": True,
        "auto_tune": True,
        "learning_rate": 0.1
    }
}
