#!/usr/bin/env python3
"""
Windows UTF-8 Console Patch for EchoFrame
Fixes Unicode console output issues on Windows
"""

import sys
import os
import locale

def setup_windows_utf8():
    """Configure Windows console for UTF-8 output"""
    if sys.platform == "win32":
        try:
            # Try to set console to UTF-8 mode
            import ctypes
            kernel32 = ctypes.windll.kernel32
            
            # Set console output code page to UTF-8
            kernel32.SetConsoleOutputCP(65001)
            
            # Set console input code page to UTF-8  
            kernel32.SetConsoleCP(65001)
            
            # Reconfigure stdout/stderr with UTF-8 encoding
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
            
            return True
        except Exception:
            # Fallback: set environment variable for future processes
            os.environ['PYTHONIOENCODING'] = 'utf-8'
            return False
    return True

def safe_print(message):
    """Print with Unicode fallback for Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Replace Unicode characters with ASCII equivalents
        safe_message = message.encode('ascii', errors='replace').decode('ascii')
        print(safe_message)

# Patch the installer to use safe printing
def patch_installer():
    """Apply Windows compatibility patches to the installer"""
    
    # Setup UTF-8 console if possible
    utf8_success = setup_windows_utf8()
    
    if not utf8_success:
        print("Note: Console UTF-8 setup failed. Using ASCII fallback for display.")
        print("Files will still be created with proper UTF-8 encoding.")
    
    return utf8_success

if __name__ == "__main__":
    print("Testing Windows UTF-8 support...")
    
    success = patch_installer()
    
    if success:
        print("✨ UTF-8 console configured successfully!")
        print("🌱 Unicode characters should display properly.")
        print("❌ This includes emoji and special symbols.")
    else:
        print("ASCII fallback mode active.")
        print("Files will still work correctly.")
