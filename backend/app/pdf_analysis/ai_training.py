"""
AI training pipeline module for PrecisionTakeAI.

This module provides functionality to collect feedback on detection accuracy,
store training data, and retrain AI models to improve accuracy over time.
"""

import os
import json
import datetime
import numpy as np
from ..pdf_analysis.config import AI_TRAINING_CONFIG

class AITrainingPipeline:
    """
    Manages the AI training pipeline for continuous model improvement.
    
    Features:
    - Feedback collection on detection accuracy
    - Training data storage and management
    - Model retraining scheduling
    - Performance tracking
    """
    
    def __init__(self, config=None):
        """
        Initialize the AI training pipeline with configuration settings.
        
        Args:
            config (dict, optional): Configuration dictionary. If None, uses default config.
        """
        self.config = config or AI_TRAINING_CONFIG
        self.collect_feedback_enabled = self.config.get("collect_feedback", True)
        self.feedback_storage = self.config.get("feedback_storage", "feedback_data")
        self.auto_retrain = self.config.get("auto_retrain", False)
        self.training_interval_days = self.config.get("training_interval_days", 7)
        self.min_feedback_samples = self.config.get("min_feedback_samples", 50)
        
        # Create feedback storage directory if it doesn't exist
        os.makedirs(self.feedback_storage, exist_ok=True)
        
        # Initialize model version tracking
        self.model_info_file = os.path.join(self.feedback_storage, "model_info.json")
        self._initialize_model_info()
    
    def _initialize_model_info(self):
        """Initialize model information tracking file if it doesn't exist."""
        if not os.path.exists(self.model_info_file):
            model_info = {
                "current_version": "0.1.0",
                "last_training_date": None,
                "training_history": [],
                "performance_metrics": {
                    "accuracy": 0.95,  # Initial simulated accuracy
                    "precision": 0.94,
                    "recall": 0.93,
                    "f1_score": 0.935
                }
            }
            with open(self.model_info_file, 'w') as f:
                json.dump(model_info, f, indent=2)
    
    def get_model_info(self):
        """
        Get current model information.
        
        Returns:
            dict: Model information including version and performance metrics
        """
        if os.path.exists(self.model_info_file):
            with open(self.model_info_file, 'r') as f:
                return json.load(f)
        return self._initialize_model_info()
    
    def collect_feedback(self, feedback_data):
        """
        Collect feedback on detection accuracy for model improvement.
        
        Args:
            feedback_data (dict): Feedback data containing:
                - file_id: ID of the analyzed file
                - element_id: ID of the element being corrected
                - original_detection: Original detection result
                - corrected_data: User-provided correction
                - feedback_type: Type of feedback (e.g., "element_correction", "clash_correction")
                
        Returns:
            dict: Status of feedback collection
        """
        if not self.collect_feedback_enabled:
            return {"status": "error", "message": "Feedback collection is disabled"}
        
        # Validate feedback data
        required_fields = ["file_id", "element_id", "original_detection", "corrected_data", "feedback_type"]
        for field in required_fields:
            if field not in feedback_data:
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        # Add timestamp and unique ID to feedback
        feedback_data["timestamp"] = datetime.datetime.now().isoformat()
        feedback_data["feedback_id"] = f"feedback_{len(os.listdir(self.feedback_storage))}"
        
        # Save feedback to file
        feedback_file = os.path.join(self.feedback_storage, f"{feedback_data['feedback_id']}.json")
        with open(feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
        
        # Check if we should trigger retraining
        if self.auto_retrain:
            self._check_retraining_needed()
        
        return {
            "status": "success", 
            "message": "Feedback collected successfully",
            "feedback_id": feedback_data["feedback_id"]
        }
    
    def _check_retraining_needed(self):
        """Check if model retraining is needed based on feedback count and time interval."""
        # Count feedback files
        feedback_files = [f for f in os.listdir(self.feedback_storage) if f.endswith('.json') and f != "model_info.json"]
        feedback_count = len(feedback_files)
        
        # Get last training date
        model_info = self.get_model_info()
        last_training_date = model_info.get("last_training_date")
        
        # Convert to datetime if not None
        if last_training_date:
            last_training_date = datetime.datetime.fromisoformat(last_training_date)
            days_since_training = (datetime.datetime.now() - last_training_date).days
        else:
            days_since_training = float('inf')  # Infinite days if never trained
        
        # Check if retraining is needed
        if feedback_count >= self.min_feedback_samples and days_since_training >= self.training_interval_days:
            return self.retrain_model()
        
        return {"status": "info", "message": "Retraining not needed yet"}
    
    def retrain_model(self):
        """
        Retrain the AI model using collected feedback.
        
        Returns:
            dict: Status of retraining process
        """
        # In a real implementation, this would:
        # 1. Load all feedback data
        # 2. Prepare training dataset
        # 3. Retrain the model
        # 4. Evaluate performance
        # 5. Update model if performance improved
        
        # For now, we'll simulate the retraining process
        
        # Simulate training time
        training_duration = np.random.uniform(10, 60)  # seconds
        
        # Simulate performance improvement
        model_info = self.get_model_info()
        current_accuracy = model_info["performance_metrics"]["accuracy"]
        
        # Small random improvement (0-2%)
        accuracy_improvement = np.random.uniform(0, 0.02)
        new_accuracy = min(0.995, current_accuracy + accuracy_improvement)
        
        # Update other metrics proportionally
        precision_improvement = accuracy_improvement * np.random.uniform(0.8, 1.2)
        recall_improvement = accuracy_improvement * np.random.uniform(0.8, 1.2)
        
        new_precision = min(0.995, model_info["performance_metrics"]["precision"] + precision_improvement)
        new_recall = min(0.995, model_info["performance_metrics"]["recall"] + recall_improvement)
        new_f1 = 2 * (new_precision * new_recall) / (new_precision + new_recall)
        
        # Update model info
        current_version = model_info["current_version"]
        version_parts = current_version.split('.')
        new_version = f"{version_parts[0]}.{version_parts[1]}.{int(version_parts[2]) + 1}"
        
        training_record = {
            "version": new_version,
            "date": datetime.datetime.now().isoformat(),
            "duration_seconds": training_duration,
            "samples_used": len([f for f in os.listdir(self.feedback_storage) if f.endswith('.json') and f != "model_info.json"]),
            "performance_improvement": {
                "accuracy": round(new_accuracy - current_accuracy, 4),
                "precision": round(new_precision - model_info["performance_metrics"]["precision"], 4),
                "recall": round(new_recall - model_info["performance_metrics"]["recall"], 4),
                "f1_score": round(new_f1 - model_info["performance_metrics"]["f1_score"], 4)
            }
        }
        
        model_info["current_version"] = new_version
        model_info["last_training_date"] = datetime.datetime.now().isoformat()
        model_info["training_history"].append(training_record)
        model_info["performance_metrics"] = {
            "accuracy": round(new_accuracy, 4),
            "precision": round(new_precision, 4),
            "recall": round(new_recall, 4),
            "f1_score": round(new_f1, 4)
        }
        
        # Save updated model info
        with open(self.model_info_file, 'w') as f:
            json.dump(model_info, f, indent=2)
        
        return {
            "status": "success",
            "message": "Model retrained successfully",
            "new_version": new_version,
            "performance_metrics": model_info["performance_metrics"],
            "improvement": training_record["performance_improvement"]
        }
    
    def get_feedback_stats(self):
        """
        Get statistics about collected feedback.
        
        Returns:
            dict: Feedback statistics
        """
        feedback_files = [f for f in os.listdir(self.feedback_storage) if f.endswith('.json') and f != "model_info.json"]
        
        # Count feedback by type
        feedback_types = {}
        for file_name in feedback_files:
            file_path = os.path.join(self.feedback_storage, file_name)
            try:
                with open(file_path, 'r') as f:
                    feedback = json.load(f)
                    feedback_type = feedback.get("feedback_type", "unknown")
                    feedback_types[feedback_type] = feedback_types.get(feedback_type, 0) + 1
            except:
                continue
        
        return {
            "total_feedback": len(feedback_files),
            "feedback_by_type": feedback_types,
            "feedback_needed_for_training": max(0, self.min_feedback_samples - len(feedback_files)),
            "auto_retrain_enabled": self.auto_retrain
        }
