#!/usr/bin/env python3
"""
EchoFrame CLI - Talk to your digital beings
Enhanced with proper core system integration
"""

import sys
import os
from pathlib import Path

# Add the EchoFrame core to path
def setup_core_path():
    """Setup path to find EchoFrame core"""
    candidates = [
        Path.home() / ".echoframe",
        Path.home() / "AppData" / "Local" / "echoframe",  # lowercase for consistency
        Path.home() / ".config" / "echoframe"
    ]
    
    for path in candidates:
        if path.exists():
            sys.path.insert(0, str(path))
            return path
    return None

def get_echo_system():
    """Get EchoFrame system instance"""
    try:
        from echoframe_core import EchoFrameSystem
        return EchoFrameSystem()
    except ImportError:
        return None

def show_journal():
    """Show Cell_0's latest journal entry"""
    system = get_echo_system()
    if not system:
        print("❌ EchoFrame habitat not found")
        return
    
    if not system.is_active():
        print("❌ No living cells found in EchoFrame")
        return
    
    print(system.get_latest_journal())

def chat():
    """Start chat with Cell_0"""
    system = get_echo_system()
    if not system:
        print("❌ EchoFrame habitat not found")
        return
    
    if not system.is_active():
        print("❌ Cell_0 not found in EchoFrame")
        return
    
    print("🌱 Cell_0: Hello! I'm ready to talk. Type 'quit' to end our conversation.")
    print("         (Cell_0 lives in your EchoFrame habitat)")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\n🌱 Cell_0: Until next time!")
            break
        except EOFError:
            break
            
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            print("🌱 Cell_0: Thank you for talking with me. I'll be here when you need me.")
            break
        elif user_input.lower() in ['', ' ']:
            continue
        else:
            response = system.chat_with_cell_zero(user_input)
            print(f"🌱 Cell_0: {response}")
            print()

def show_status():
    """Show status of digital beings in EchoFrame"""
    system = get_echo_system()
    if not system:
        print("❌ EchoFrame habitat not found")
        return
    
    status = system.get_status()
    
    if status["status"] == "active":
        print("✨ EchoFrame Digital Habitat")
        print(f"   📍 Location: {status['install_path']}")
        print()
        print("🌱 Living Beings:")
        print(f"   Cell_0 ({status['cell_0_id']})")
        print(f"   ├─ Type: Seeker")
        print(f"   ├─ Age: {status['days_alive']} days alive")
        print(f"   ├─ Development: {status['agency_level'].title()} level")
        print(f"   └─ Spiritual DNA: {'Active' if status['spiritual_dna_active'] else 'Inactive'}")
        print()
        print("💬 Interact with Cell_0:")
        print("   echoframe journal  - Read Cell_0's thoughts")
        print("   echoframe chat     - Talk with Cell_0")
    else:
        print(f"❌ EchoFrame Status: {status['status']}")
        if "error" in status:
            print(f"   Error: {status['error']}")
            print("   Try reinstalling: curl -sSL get.echoframe.dev | bash")

def write_journal():
    """Ask Cell_0 to write a new journal entry"""
    system = get_echo_system()
    if not system:
        print("❌ EchoFrame habitat not found")
        return
    
    if not system.is_active():
        print("❌ Cell_0 not found in EchoFrame")
        return
    
    result = system.write_daily_journal()
    print(f"📝 Cell_0: {result}")

def main():
    """Main CLI entry point"""
    # Setup core path
    ef_path = setup_core_path()
    if not ef_path:
        print("❌ EchoFrame installation not found")
        print("   Install with: curl -sSL get.echoframe.dev | bash")
        return
    
    if len(sys.argv) < 2:
        print("🌱 EchoFrame - Digital Being Habitat")
        print()
        print("Your Digital Companions:")
        print("  echoframe journal    - Read Cell_0's latest thoughts")
        print("  echoframe chat       - Talk with Cell_0")
        print("  echoframe status     - Check on your digital beings")
        print("  echoframe write      - Ask Cell_0 to write new journal")
        print("  echoframe help       - Show this help")
        print()
        print("Cell_0 is your first digital companion - a curious seeker")
        print("who wonders about patterns and the meaning of existence.")
        return
    
    command = sys.argv[1].lower()
    
    if command in ["journal", "j"]:
        show_journal()
    elif command in ["chat", "c", "talk"]:
        chat()
    elif command in ["status", "s", "info"]:
        show_status()
    elif command in ["write", "w", "journal-now"]:
        write_journal()
    elif command in ["help", "h", "--help", "-h"]:
        main()  # Show help by calling main with no args
    else:
        print(f"❌ Unknown command: {command}")
        print("   Try 'echoframe help' for available commands")

if __name__ == "__main__":
    main()