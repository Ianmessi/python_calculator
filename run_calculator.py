#!/usr/bin/env python3
"""
Python Calculator Runner
------------------------
This script detects available dependencies and runs the appropriate version
of the Python Calculator (either web-based with Streamlit or desktop with PyQt).
"""

import os
import sys
import subprocess
import importlib.util

def check_module(module_name):
    """Check if a Python module is installed."""
    return importlib.util.find_spec(module_name) is not None

def get_python_executable():
    """Get the appropriate Python executable path."""
    return sys.executable

def run_streamlit_app():
    """Run the Streamlit web app version of the calculator."""
    print("Starting Python Calculator (Web Version)...")
    python_exec = get_python_executable()
    
    # Check if streamlit is in PATH or in user's Python path
    streamlit_in_path = False
    try:
        subprocess.run(["streamlit", "--version"], capture_output=True, check=False)
        streamlit_in_path = True
    except FileNotFoundError:
        # Check common locations for streamlit
        common_paths = [
            os.path.expanduser("~/Library/Python/3.9/bin/streamlit"),
            os.path.expanduser("~/Library/Python/3.8/bin/streamlit"),
            os.path.expanduser("~/.local/bin/streamlit"),
        ]
        for path in common_paths:
            if os.path.exists(path):
                streamlit_command = path
                break
        else:
            streamlit_command = "streamlit"  # Will likely fail but worth trying
    
    if streamlit_in_path:
        cmd = ["streamlit", "run", "app.py"]
    else:
        cmd = [python_exec, "-m", "streamlit", "run", "app.py"]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Error running Streamlit app. Trying alternative method...")
        # Try alternative way to run streamlit
        try:
            subprocess.run([streamlit_command, "run", "app.py"], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Failed to run Streamlit app. Please make sure Streamlit is installed:")
            print("pip install streamlit")
            print("\nAlternatively, try opening the desktop calculator.")
            return False
    
    return True

def run_desktop_app():
    """Run the desktop PyQt version of the calculator."""
    print("Starting Python Calculator (Desktop Version)...")
    python_exec = get_python_executable()
    
    try:
        subprocess.run([python_exec, "pyqt_calculator.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error running desktop calculator.")
        return False

def main():
    """Main function to determine which calculator to run."""
    print("Python Calculator Runner")
    print("=======================")
    print("Checking available dependencies...")
    
    web_available = check_module("streamlit")
    desktop_available = check_module("PyQt5")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        # User explicitly requested web version
        if web_available:
            run_streamlit_app()
        else:
            print("Streamlit is not installed. Please install it with:")
            print("pip install streamlit")
            print("\nAttempting to run desktop version instead...")
            if desktop_available:
                run_desktop_app()
            else:
                print("Desktop version dependencies (PyQt5) are also not available.")
                print("Please install either Streamlit or PyQt5.")
    
    elif len(sys.argv) > 1 and sys.argv[1] == "--desktop":
        # User explicitly requested desktop version
        if desktop_available:
            run_desktop_app()
        else:
            print("PyQt5 is not installed. Please install it with:")
            print("pip install PyQt5")
            print("\nAttempting to run web version instead...")
            if web_available:
                run_streamlit_app()
            else:
                print("Web version dependencies (Streamlit) are also not available.")
                print("Please install either PyQt5 or Streamlit.")
    
    else:
        # Auto-detect - prefer desktop on Mac/Windows, web otherwise
        print("Available calculator versions:")
        if web_available:
            print("- Web version (Streamlit): Available")
        else:
            print("- Web version (Streamlit): Not available")
        
        if desktop_available:
            print("- Desktop version (PyQt): Available")
        else: 
            print("- Desktop version (PyQt): Not available")
        
        print("\nStarting calculator...")
        
        if sys.platform in ['darwin', 'win32'] and desktop_available:
            # On Mac or Windows, prefer desktop app if available
            success = run_desktop_app()
            if not success and web_available:
                run_streamlit_app()
        elif web_available:
            # On other platforms or if desktop not available, use web app
            success = run_streamlit_app()
            if not success and desktop_available:
                run_desktop_app()
        else:
            print("Neither Streamlit nor PyQt5 is installed.")
            print("Please install one of them to run the calculator:")
            print("For web version: pip install streamlit")
            print("For desktop version: pip install PyQt5")

if __name__ == "__main__":
    main() 