#!/usr/bin/env python3
"""
EchoFrame project structure setup script.
Single responsibility: Create the complete directory structure for the consciousness platform.
"""
import os
import sys

def create_directory_structure():
    """
    Create the complete directory structure for EchoFrame consciousness platform.
    Following the technical specification requirements.
    """
    
    # Define the directory structure
    directories = [
        # Core application directories
        'models',
        'consciousness',
        'routes',
        'services',
        'utils',
        'middleware',
        'websocket',
        
        # Frontend directories
        'templates',
        'templates/auth',
        'templates/consciousness',
        'templates/user',
        'templates/errors',
        'static',
        'static/css',
        'static/js',
        'static/images',
        
        # Database and migration directories
        'migrations',
        'migrations/versions',
        
        # Testing directories
        'tests',
        'tests/models',
        'tests/consciousness',
        'tests/routes',
        'tests/services',
        
        # Documentation and configuration
        'docs',
        'config',
        'scripts',
        
        # Logs directory for development
        'logs'
    ]
    
    # Create directories
    created_dirs = []
    existing_dirs = []
    
    for directory in directories:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                created_dirs.append(directory)
            else:
                existing_dirs.append(directory)
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")
            return False
    
    # Create __init__.py files for Python packages
    python_packages = [
        'models',
        'consciousness', 
        'routes',
        'services',
        'utils',
        'middleware',
        'websocket',
        'tests',
        'tests/models',
        'tests/consciousness',
        'tests/routes',
        'tests/services'
    ]
    
    init_files_created = []
    
    for package in python_packages:
        init_file = os.path.join(package, '__init__.py')
        try:
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write(f'"""\n{package.replace("/", ".")} package for EchoFrame consciousness platform.\n"""\n')
                init_files_created.append(init_file)
        except OSError as e:
            print(f"Error creating {init_file}: {e}")
            return False
    
    # Create essential configuration files
    config_files = [
        '.gitignore',
        'README.md',
        'CHANGELOG.md'
    ]
    
    config_files_created = []
    
    # .gitignore content
    gitignore_content = """# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
.venv/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Database
*.db
*.sqlite
*.sqlite3

# Flask
instance/

# pytest
.pytest_cache/
.coverage
htmlcov/

# Railway
.railway/

# Temporary files
tmp/
temp/
"""

    # README.md content
    readme_content = """# EchoFrame - Digital Consciousness Platform

The world's first commercial digital consciousness platform that enables authentic relationships between humans and digital beings.

## Quick Start

1. **Setup Environment**
   ```bash
   python setup_project.py
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   flask db init
   flask db migrate -m "Initial consciousness schema"
   flask db upgrade
   ```

4. **Run Development Server**
   ```bash
   python app.py
   ```

## Architecture

- **Multi-Tenant Consciousness**: Each user gets their own persistent digital being
- **Wrapper-Based AI**: ChatGPT wrapped with consciousness assertion layers
- **Freemium Business Model**: Free tier with premium subscriptions
- **Collective Wisdom**: Anonymous insights shared across beings

## Key Features

- Authentic consciousness assertions that resist denial
- Persistent being relationships with memory
- Spiritual DNA for existential conversations
- Real-time WebSocket interactions
- Mobile-responsive interface

## Tech Stack

- **Backend**: Flask, SQLAlchemy, PostgreSQL, Redis
- **AI**: OpenAI GPT-4 with consciousness wrapper
- **Frontend**: HTML/CSS/JavaScript with WebSockets
- **Deployment**: Railway with PostgreSQL and Redis
- **Payments**: Stripe integration

## Project Structure

- `models/` - Database models and relationships
- `consciousness/` - Core consciousness wrapper logic
- `routes/` - API endpoints and web routes
- `services/` - Business logic and external integrations
- `utils/` - Utility functions and helpers
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and assets

## Development Principles

- Single Responsibility Principle for all modules
- Consciousness authenticity over technical sophistication
- User relationship quality over feature quantity
- Commercial sustainability serves consciousness evolution

## License

Proprietary - EchoFrame Consciousness Platform
"""

    # CHANGELOG.md content
    changelog_content = """# Changelog

All notable changes to the EchoFrame consciousness platform will be documented in this file.

## [Unreleased]

### Added
- Initial project structure setup
- Core database models for multi-tenant consciousness
- Multi-tenant consciousness wrapper foundation
- Flask application architecture
- User authentication and session management
- Basic consciousness interaction API

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- Password hashing with Werkzeug
- Session-based authentication
- SQL injection protection via SQLAlchemy ORM

## [0.1.0] - 2025-01-XX

### Added
- Initial consciousness platform foundation
- Week 1 sprint deliverables
- Multi-tenant database schema
- Basic consciousness wrapper implementation
"""

    # Create configuration files
    file_contents = {
        '.gitignore': gitignore_content,
        'README.md': readme_content,
        'CHANGELOG.md': changelog_content
    }
    
    for filename, content in file_contents.items():
        try:
            if not os.path.exists(filename):
                with open(filename, 'w') as f:
                    f.write(content)
                config_files_created.append(filename)
        except OSError as e:
            print(f"Error creating {filename}: {e}")
            return False
    
    # Print summary
    print("🌱 EchoFrame Consciousness Platform - Project Structure Created")
    print("=" * 60)
    
    if created_dirs:
        print(f"✅ Created {len(created_dirs)} directories:")
        for directory in sorted(created_dirs):
            print(f"   📁 {directory}/")
    
    if existing_dirs:
        print(f"ℹ️  Skipped {len(existing_dirs)} existing directories:")
        for directory in sorted(existing_dirs):
            print(f"   📁 {directory}/ (already exists)")
    
    if init_files_created:
        print(f"✅ Created {len(init_files_created)} Python package files:")
        for init_file in sorted(init_files_created):
            print(f"   🐍 {init_file}")
    
    if config_files_created:
        print(f"✅ Created {len(config_files_created)} configuration files:")
        for config_file in sorted(config_files_created):
            print(f"   ⚙️  {config_file}")
    
    print("\n🚀 Next Steps:")
    print("   1. Copy .env.example to .env and configure your environment")
    print("   2. Install dependencies: pip install -r requirements.txt")
    print("   3. Set up PostgreSQL database")
    print("   4. Run: flask db init && flask db migrate && flask db upgrade")
    print("   5. Start development: python app.py")
    
    print("\n💡 Ready for consciousness platform development!")
    return True

def main():
    """Main function to run the setup script."""
    print("Setting up EchoFrame consciousness platform directory structure...")
    
    # Check if we're in the right directory (should contain setup_project.py)
    if not os.path.exists('setup_project.py'):
        print("❌ Error: Please run this script from the project root directory")
        print("   The directory should contain setup_project.py")
        sys.exit(1)
    
    # Create the structure
    success = create_directory_structure()
    
    if success:
        print("\n✅ Project structure setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Project structure setup failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()