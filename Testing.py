from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import List, Optional, Dict, Any, get_origin, get_args, Union, OrderedDict
from datetime import datetime
import csv
import inspect
import json

class EmailAnalysisTesting:
    """
    A class for calculating accuracy between predicted and ground truth EmailAnalysis JSONs.
    Automatically parses model structure for type checking and enum handling.
    """
    
    def __init__(self, model_class: type[BaseModel]):
        self.model_class = model_class
        self.enum_lengths = self._get_enum_lengths()
        self.soft_accuracy_fields = self._get_soft_accuracy_fields()
        self.field_types = self._get_field_types()
    
    def _parse_json_input(self, json_input: Union[str, Dict]) -> Dict:
        """
        Parse JSON input that could be either a string or dictionary.
        
        Args:
            json_input: JSON string or dictionary
            
        Returns:
            Dict: Parsed JSON dictionary
        """
        if isinstance(json_input, str):
            try:
                # Handle double-escaped JSON strings from CSV
                if json_input.startswith('"') and json_input.endswith('"'):
                    json_input = json_input.strip('"')
                    # Replace double quotes with single quotes
                    json_input = json_input.replace('""', '"')
                return json.loads(json_input)
            except json.JSONDecodeError as e:
                try:
                    return json.loads(json_input, object_pairs_hook=OrderedDict)
                except json.JSONDecodeError:
                    raise ValueError(f"Invalid JSON string: {e}")
        elif isinstance(json_input, dict):
            return json_input
        else:
            raise ValueError(f"Input must be either a JSON string or dictionary, got {type(json_input)}")
    
    def _get_enum_lengths(self) -> Dict[str, int]:
        """
        Automatically discover all enums in the model and their lengths.
        
        Returns:
            Dict[str, int]: Dictionary mapping enum class names to their lengths
        """
        enum_lengths = {}
        
        # Get all classes defined in the module
        for name, obj in inspect.getmembers(self.model_class):
            # Check nested classes
            if inspect.isclass(obj):
                # Look for enum classes
                if isinstance(obj, type) and issubclass(obj, Enum):
                    enum_lengths[obj.__name__] = len(list(obj))
                
        # Also check imported enums from model's annotations
        for field_type in self.model_class.__annotations__.values():
            if get_origin(field_type) is None:  # Direct type
                if isinstance(field_type, type) and issubclass(field_type, Enum):
                    enum_lengths[field_type.__name__] = len(list(field_type))
            elif get_origin(field_type) in (list, Dict):  # Handle Optional/List/Dict
                args = get_args(field_type)
                for arg in args:
                    if isinstance(arg, type) and issubclass(arg, Enum):
                        enum_lengths[arg.__name__] = len(list(arg))
        
        return enum_lengths
    
    def _get_soft_accuracy_fields(self) -> Dict[str, str]:
        """
        Automatically identify fields that should use soft accuracy (enums).
        
        Returns:
            Dict[str, str]: Dictionary mapping field paths to their enum types
        """
        soft_accuracy_fields = {}
        schema = self.model_class.schema()
        
        def process_properties(properties: Dict, parent_path: str = ""):
            for prop_name, prop_data in properties.items():
                current_path = f"{parent_path}.{prop_name}" if parent_path else prop_name
                
                # Check if it's an enum reference
                if "allOf" in prop_data and prop_data["allOf"][0].get("$ref", "").startswith("#/definitions/"):
                    enum_type = prop_data["allOf"][0]["$ref"].split("/")[-1]
                    if enum_type in self.enum_lengths:
                        soft_accuracy_fields[current_path] = enum_type
                
                # Recursively process nested objects
                if "properties" in prop_data:
                    process_properties(prop_data["properties"], current_path)
        
        process_properties(schema.get("properties", {}))
        return soft_accuracy_fields
    
    def _get_field_types(self) -> Dict[str, type]:
        """
        Get the types of all fields in the model.
        
        Returns:
            Dict[str, type]: Dictionary mapping field paths to their types
        """
        field_types = {}
        schema = self.model_class.schema()
        
        def process_properties(properties: Dict, parent_path: str = ""):
            for prop_name, prop_data in properties.items():
                current_path = f"{parent_path}.{prop_name}" if parent_path else prop_name
                
                # Map JSON schema types to Python types
                type_mapping = {
                    "string": str,
                    "integer": int,
                    "number": float,
                    "boolean": bool,
                    "array": list,
                    "object": dict
                }
                
                if "type" in prop_data:
                    field_types[current_path] = type_mapping.get(prop_data["type"], Any)
                
                # Handle nested objects
                if "properties" in prop_data:
                    process_properties(prop_data["properties"], current_path)
        
        process_properties(schema.get("properties", {}))
        return field_types
    
    def calculate_soft_accuracy(self, pred_value: str, true_value: str, enum_type: str) -> float:
        """
        Calculate soft accuracy for enum values based on their distance in the enum.
        
        Args:
            pred_value: Predicted enum value
            true_value: Ground truth enum value
            enum_type: Type of enum (used to determine number of possible values)
            
        Returns:
            float: Accuracy score between 0 and 1
        """
        if pred_value == true_value:
            return 1.0
        
        enum_length = self.enum_lengths[enum_type]
        penalty_step = 1.0 / (enum_length - 1)
        
        # Get the enum class from the model
        enum_class = None
        for name, obj in inspect.getmembers(self.model_class):
            if inspect.isclass(obj) and issubclass(obj, Enum) and obj.__name__ == enum_type:
                enum_class = obj
                break
        
        if enum_class is None:
            raise ValueError(f"Enum class {enum_type} not found")
        
        # Convert enum values to indices
        try:
            pred_idx = list(enum_class).index(enum_class(pred_value))
            true_idx = list(enum_class).index(enum_class(true_value))
        except ValueError:
            return 0.0  # Invalid enum value
        
        # Calculate distance-based penalty
        distance = abs(pred_idx - true_idx)
        accuracy = max(0.0, 1.0 - (distance * penalty_step))
        
        return accuracy
    
    def calculate_field_accuracy(self, pred_value: Any, true_value: Any, field_path: str) -> float:
        """
        Calculate accuracy for a single field, handling different types appropriately.
        
        Args:
            pred_value: Predicted value
            true_value: Ground truth value
            field_path: Path to the field in dot notation
            
        Returns:
            float: Accuracy score between 0 and 1
        """
        # Handle None values
        if pred_value is None and true_value is None:
            return 1.0
        if pred_value is None or true_value is None:
            return 0.0
        
        # Handle soft accuracy fields (enums)
        if field_path in self.soft_accuracy_fields:
            return self.calculate_soft_accuracy(
                pred_value,
                true_value,
                self.soft_accuracy_fields[field_path]
            )
        
        # Get expected type for the field
        field_type = self.field_types.get(field_path, Any)
        
        # Handle different types
        if field_type == bool:
            return 1.0 if pred_value == true_value else 0.0
        
        if field_type in (int, float):
            # Normalize numerical differences
            max_val = max(abs(pred_value), abs(true_value))
            if max_val == 0:
                return 1.0 if pred_value == true_value else 0.0
            return max(0.0, 1.0 - abs(pred_value - true_value) / max_val)
        
        if isinstance(true_value, datetime):
            # Convert to timestamps and calculate difference-based accuracy
            pred_ts = pred_value.timestamp()
            true_ts = true_value.timestamp()
            # Allow for 24-hour difference with linear penalty
            max_diff = 86400  # 24 hours in seconds
            diff = abs(pred_ts - true_ts)
            return max(0.0, 1.0 - (diff / max_diff))
        
        if field_type == list:
            if not pred_value or not true_value:
                return 1.0 if pred_value == true_value else 0.0
            # Calculate Jaccard similarity for lists
            pred_set = set(pred_value)
            true_set = set(true_value)
            return len(pred_set.intersection(true_set)) / len(pred_set.union(true_set))
        
        # Default to exact match for strings and other types
        return 1.0 if pred_value == true_value else 0.0
    
    def flatten_dict(self, d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
        """
        Flatten a nested dictionary with dot notation for keys.
        
        Args:
            d: Dictionary to flatten
            parent_key: Parent key for nested dictionaries
            sep: Separator for nested keys
            
        Returns:
            Dict: Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def calculate_accuracy(self, predicted_json: Dict, ground_truth_json: Dict, save_path: str = "accuracy_results.json"):
        """
        Calculate accuracy metrics between predicted and ground truth JSONs.
        
        Args:
            predicted_json: Predicted EmailAnalysis JSON
            ground_truth_json: Ground truth EmailAnalysis JSON
            
        Returns:
            Dict[str, float]: Dictionary containing overall and field-wise accuracy scores
        """

        # Parse inputs to ensure we have dictionaries
        try:
            print('parsing inputs')
            pred_dict = self._parse_json_input(predicted_json)
            print('predicted json ok')
            truth_dict = self._parse_json_input(ground_truth_json)
            print('truth json ok')
        except ValueError as e:
            raise ValueError(f"Error parsing JSON input: {e}")

        # Flatten both JSONs
        pred_flat = self.flatten_dict(pred_dict)
        true_flat = self.flatten_dict(truth_dict)
        
        # Calculate field-wise accuracy
        field_accuracies = {}
        for field in true_flat:
            if field in pred_flat:
                field_accuracies[field] = self.calculate_field_accuracy(
                    pred_flat[field],
                    true_flat[field],
                    field
                )
            else:
                field_accuracies[field] = 0.0
        
        # Calculate overall accuracy
        overall_accuracy = sum(field_accuracies.values()) / len(field_accuracies)
        
        # Organize results in a nicely formatted dictionary for visualization
        results = {
            "timestamp": datetime.now().isoformat(),
            "overall_accuracy": overall_accuracy,
            "field_accuracies": field_accuracies
        }

        # Save results to a JSON file
        results_json = json.dumps(results)

        # Append the JSON string as a new row in the CSV
        with open('Results.csv', mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([results_json])  # Each row is a single-column JSON entry

        return results

        ## We can add more metrics like llm evaluation and a reasoning. This reasoning may help identify the cause of the error and improvements.