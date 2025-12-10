#!/usr/bin/env python3
"""
Quick validation script to test the Generative UI template setup.

This script checks:
- Python dependencies are installed
- API keys are configured
- Backend can start
- UI generation works
"""

import sys
import importlib
from pathlib import Path


def print_status(message, status="info"):
    """Print colored status message."""
    colors = {
        "info": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m",
        "reset": "\033[0m"
    }
    
    symbols = {
        "info": "ℹ",
        "success": "✓",
        "warning": "⚠",
        "error": "✗"
    }
    
    color = colors.get(status, colors["info"])
    symbol = symbols.get(status, "")
    reset = colors["reset"]
    
    print(f"{color}{symbol} {message}{reset}")


def check_python_version():
    """Check Python version is compatible."""
    print_status("Checking Python version...", "info")
    
    version = sys.version_info
    if version.major == 3 and 10 <= version.minor <= 13:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Compatible", "success")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Incompatible (need 3.10-3.13)", "error")
        return False


def check_dependencies():
    """Check required Python packages are installed."""
    print_status("Checking dependencies...", "info")
    
    required = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("autogen", "AG2/AutoGen"),
        ("jinja2", "Jinja2"),
    ]
    
    all_installed = True
    for module_name, display_name in required:
        try:
            importlib.import_module(module_name)
            print_status(f"{display_name} installed", "success")
        except ImportError:
            print_status(f"{display_name} NOT installed", "error")
            all_installed = False
    
    return all_installed


def check_api_keys():
    """Check if API keys are configured."""
    print_status("Checking API configuration...", "info")
    
    import os
    
    has_config = False
    
    # Check environment variable
    if os.getenv("OPENAI_API_KEY"):
        print_status("OPENAI_API_KEY environment variable found", "success")
        has_config = True
    
    # Check OAI_CONFIG_LIST file
    if Path("OAI_CONFIG_LIST").exists():
        print_status("OAI_CONFIG_LIST file found", "success")
        has_config = True
    
    if not has_config:
        print_status("No API configuration found", "warning")
        print_status("Set OPENAI_API_KEY or create OAI_CONFIG_LIST file", "info")
        return False
    
    return True


def check_file_structure():
    """Check template file structure is intact."""
    print_status("Checking file structure...", "info")
    
    required_paths = [
        "backend/main.py",
        "backend/agents.py",
        "backend/ui_generator.py",
        "frontend/templates/index.html",
        "frontend/static/css/styles.css",
        "frontend/static/js/app.js",
        "requirements.txt",
    ]
    
    all_present = True
    for path in required_paths:
        if Path(path).exists():
            print_status(f"Found {path}", "success")
        else:
            print_status(f"Missing {path}", "error")
            all_present = False
    
    return all_present


def test_ui_generation():
    """Test basic UI generation."""
    print_status("Testing UI generation...", "info")
    
    try:
        from backend.ui_generator import UIGenerator
        
        generator = UIGenerator()
        
        # Test form generation
        form_ui = generator.generate(
            intent="create a simple form",
            context={},
            agents={}
        )
        
        if form_ui and "type" in form_ui:
            print_status(f"Generated UI type: {form_ui['type']}", "success")
            return True
        else:
            print_status("UI generation returned invalid data", "error")
            return False
            
    except Exception as e:
        print_status(f"UI generation failed: {str(e)}", "error")
        return False


def main():
    """Run all validation checks."""
    print("\n" + "=" * 60)
    print("Generative UI Template - Validation")
    print("=" * 60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("API Configuration", check_api_keys),
        ("File Structure", check_file_structure),
        ("UI Generation", test_ui_generation),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_status(f"Check failed with error: {str(e)}", "error")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "success" if result else "error"
        print_status(f"{name}: {'PASS' if result else 'FAIL'}", status)
    
    print(f"\n{passed}/{total} checks passed\n")
    
    if passed == total:
        print_status("All checks passed! Your setup is ready.", "success")
        print_status("Run: python backend/main.py", "info")
    else:
        print_status("Some checks failed. Please fix the issues above.", "warning")
        print_status("See README.md for setup instructions", "info")
    
    print()
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
