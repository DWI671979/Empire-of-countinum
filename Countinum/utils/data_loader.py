"""
Data loader utility for robust JSON file loading
Handles different working directories and environments
"""

import json
import os
from pathlib import Path


def get_data_directory():
    """
    Get the data directory path, handling different working contexts
    """
    # Try current file location first
    current_file = Path(__file__).resolve()
    data_dir = current_file.parent.parent / "data"
    
    if data_dir.exists():
        return data_dir
    
    # Try from Countinum directory
    countinum_dir = Path.cwd()
    if countinum_dir.name == "Countinum":
        data_dir = countinum_dir / "data"
        if data_dir.exists():
            return data_dir
    
    # Try from parent of Countinum
    parent_dir = Path.cwd().parent
    if (parent_dir / "Countinum" / "data").exists():
        return parent_dir / "Countinum" / "data"
    
    # Fallback to relative path
    return Path(__file__).parent.parent / "data"


def load_json_file(filename):
    """
    Load a JSON file from the data directory
    
    Args:
        filename: Name of the JSON file (e.g., 'wiki_articles.json')
    
    Returns:
        Parsed JSON data or empty list if file not found
    """
    data_dir = get_data_directory()
    file_path = data_dir / filename
    
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"Warning: Data file not found at {file_path}")
            return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {filename}: {e}")
        return []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []


def load_wiki_articles():
    """Load wiki articles data"""
    return load_json_file("wiki_articles.json")


def load_user_profiles():
    """Load user profiles data"""
    return load_json_file("user_profiles.json")


def load_publications():
    """Load publications data"""
    return load_json_file("publications.json")


def load_announcements():
    """Load announcements data"""
    return load_json_file("announcements.json")


def load_featured():
    """Load featured data"""
    return load_json_file("featured.json")
