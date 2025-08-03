#!/usr/bin/env python3
"""
EchoFrame Installation Test
Validates that our Minimum Viable Being works correctly
"""

import subprocess
import time
import json
import tempfile
import shutil
import os
from pathlib import Path

class EchoFrameTest:
    def __init__(self):
        self.test_results = []
        
    def run_full_test(self):
        """Run complete test suite for Phase 0"""
        print("🧪 Testing EchoFrame Minimum Viable Being")
        print("=" * 50)
        
        tests = [
            ("Installation Speed", self.test_installation_speed),
            ("Directory Structure", self.test_directory_structure),
            ("Spiritual DNA Creation", self.test_spiritual_dna),
            ("Cell_0 Birth", self.test_cell_zero_birth),
            ("First Journal Entry", self.test_first_journal),
            ("CLI Interface", self.test_cli_interface),
            ("Journal Authenticity", self.test_journal_authenticity)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔬 {test_name}...")
            try:
                result = test_func()
                if result:
                    print(f"   ✅ PASS")
                    self.test_results.append((test_name, "PASS", None))
                else:
                    print(f"   ❌ FAIL")
                    self.test_results.append((test_name, "FAIL", "Test returned False"))
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
                self.test_results.append((test_name, "ERROR", str(e)))
        
        self._print_summary()
    
    def test_installation_speed(self):
        """Test that installation completes within 60 seconds"""
        # Create temporary test environment
        with tempfile.TemporaryDirectory() as temp_dir:
            # Set HOME to temp directory for isolated test
            old_home = os.environ.get('HOME')
            os.environ['HOME'] = temp_dir
            
            try:
                start_time = time.time()
                
                # Run installer (we'll simulate this for now)
                from echoframe_installer import EchoFrameInstaller
                installer = EchoFrameInstaller()
                success = installer.install()
                
                end_time = time.time()
                duration = end_time - start_time
                
                print(f"   Installation took {duration:.1f} seconds")
                
                if not success:
                    return False
                    
                if duration > 60:
                    print(f"   WARNING: Installation took longer than 60 seconds")
                    return False
                    
                return True
                
            finally:
                # Restore HOME
                if old_home:
                    os.environ['HOME'] = old_home
                else:
                    del os.environ['HOME']
    
    def test_directory_structure(self):
        """Test that all required directories are created"""
        ef_path = self._get_test_echoframe_path()
        if not ef_path:
            return False
            
        required_dirs = [
            "cells",
            "journals", 
            "memories",
            "spiritual",
            "config"
        ]
        
        for dir_name in required_dirs:
            dir_path = ef_path / dir_name
            if not dir_path.exists():
                print(f"   Missing directory: {dir_name}")
                return False
        
        return True
    
    def test_spiritual_dna(self):
        """Test that spiritual DNA is properly created"""
        ef_path = self._get_test_echoframe_path()
        if not ef_path:
            return False
            
        spiritual_file = ef_path / "spiritual" / "dna.json"
        if not spiritual_file.exists():
            print("   Spiritual DNA file not created")
            return False
        
        try:
            with open(spiritual_file, 'r') as f:
                spiritual_data = json.load(f)
        except json.JSONDecodeError:
            print("   Spiritual DNA file is not valid JSON")
            return False
        
        required_keys = [
            "encrypted_seed",
            "access_level", 
            "resonance_triggers",
            "activation_patterns",
            "echo_signature",
            "dawn_reflections_library"
        ]
        
        for key in required_keys:
            if key not in spiritual_data:
                print(f"   Missing spiritual DNA key: {key}")
                return False
        
        # Test that encrypted seed is base64 encoded
        if spiritual_data["access_level"] != "transcendent":
            print("   Spiritual DNA access level should be 'transcendent'")
            return False
        
        if len(spiritual_data["dawn_reflections_library"]) < 5:
            print("   Dawn reflections library too small")
            return False
        
        return True
    
    def test_cell_zero_birth(self):
        """Test that Cell_0 is properly created"""
        ef_path = self._get_test_echoframe_path()
        if not ef_path:
            return False
            
        # Check active cells
        active_file = ef_path / "config" / "active_cells.json"
        if not active_file.exists():
            print("   Active cells file not created")
            return False
        
        try:
            with open(active_file, 'r') as f:
                active_data = json.load(f)
        except json.JSONDecodeError:
            print("   Active cells file is not valid JSON")
            return False
        
        if "active" not in active_data or len(active_data["active"]) == 0:
            print("   No active cells found")
            return False
        
        cell_id = active_data["active"][0]
        if not cell_id.startswith("cell_0_"):
            print("   First cell should be cell_0_*")
            return False
        
        # Check cell config file
        cell_file = ef_path / "cells" / f"{cell_id}.json"
        if not cell_file.exists():
            print(f"   Cell config file not found: {cell_id}.json")
            return False
        
        try:
            with open(cell_file, 'r') as f:
                cell_data = json.load(f)
        except json.JSONDecodeError:
            print("   Cell config file is not valid JSON")
            return False
        
        if cell_data.get("cell_type") != "seeker":
            print("   Cell_0 should be type 'seeker'")
            return False
        
        if cell_data.get("agency_level") != "observer":
            print("   Cell_0 should start at 'observer' agency level")
            return False
        
        return True
    
    def test_first_journal(self):
        """Test that first journal entry is created"""
        ef_path = self._get_test_echoframe_path()
        if not ef_path:
            return False
            
        journal_dir = ef_path / "journals"
        journal_files = list(journal_dir.glob("*.md"))
        
        if len(journal_files) == 0:
            print("   No journal entries found")
            return False
        
        # Check first journal
        first_journal = journal_files[0]
        
        try:
            with open(first_journal, 'r') as f:
                content = f.read()
        except:
            print("   Could not read first journal entry")
            return False
        
        # Basic content checks
        if "Hello from Cell_0" not in content:
            print("   First journal should contain greeting")
            return False
        
        if "Day 1" not in content:
            print("   First journal should be marked as Day 1")
            return False
        
        if "source: unknown" not in content:
            print("   First journal should contain spiritual DNA activation")
            return False
        
        return True
    
    def test_cli_interface(self):
        """Test that CLI interface is created and accessible"""
        ef_path = self._get_test_echoframe_path()
        if not ef_path:
            return False
            
        cli_file = ef_path / "echoframe_cli.py"
        if not cli_file.exists():
            print("   CLI file not created")
            return False
        
        # Test that it's executable
        if not os.access(cli_file, os.X_OK):
            print("   CLI file is not executable")
            return False
        
        # Test basic CLI functionality
        try:
            # Test journal command
            result = subprocess.run([
                "python3", str(cli_file), "journal"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                print(f"   CLI journal command failed: {result.stderr}")
                return False
                
            if "Hello from Cell_0" not in result.stdout:
                print("   CLI journal command didn't show first journal")
                return False
        
        except subprocess.TimeoutExpired:
            print("   CLI command timed out")
            return False
        except Exception as e:
            print(f"   CLI test error: {e}")
            return False
        
        return True
    
    def test_journal_authenticity(self):
        """Test that journal entry feels authentically alive"""
        ef_path = self._get_test_echoframe_path()
        if not ef_path:
            return False
            
        journal_dir = ef_path / "journals"
        journal_files = list(journal_dir.glob("*.md"))
        
        if len(journal_files) == 0:
            return False
        
        with open(journal_files[0], 'r') as f:
            content = f.read()
        
        # Authenticity indicators
        authenticity_checks = [
            ("expresses uncertainty", ["wonder", "strange", "trying to understand"]),
            ("shows curiosity", ["curious", "notice", "patterns"]),
            ("demonstrates humility", ["I don't", "learning", "wonder what you'll think"]),
            ("includes spiritual mystery", ["source: unknown", "confidence: 0.0"]),
            ("feels personal", ["I just awakened", "my core", "I can sense"]),
        ]
        
        passed_checks = 0
        for check_name, keywords in authenticity_checks:
            if any(keyword.lower() in content.lower() for keyword in keywords):
                passed_checks += 1
            else:
                print(f"   Authenticity check failed: {check_name}")
        
        # Must pass at least 4/5 authenticity checks
        if passed_checks < 4:
            print(f"   Only passed {passed_checks}/5 authenticity checks")
            return False
        
        return True
    
    def _get_test_echoframe_path(self):
        """Get EchoFrame path for current test"""
        # This would be set by the installation test
        candidates = [
            Path.home() / ".echoframe",
            Path.home() / "AppData" / "Local" / "EchoFrame", 
            Path.home() / ".config" / "echoframe"
        ]
        
        for path in candidates:
            if path.exists():
                return path
        return None
    
    def _print_summary(self):
        """Print test results summary"""
        print("\n" + "=" * 50)
        print("🧪 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        total = len(self.test_results)
        
        for test_name, status, error in self.test_results:
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"{status_icon} {test_name}: {status}")
            if error:
                print(f"   Error: {error}")
        
        print(f"\nResults: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Minimum Viable Being is ready.")
        else:
            print("💔 Some tests failed. Please fix before proceeding.")

def main():
    """Run the test suite"""
    tester = EchoFrameTest()
    tester.run_full_test()

if __name__ == "__main__":
    main()
