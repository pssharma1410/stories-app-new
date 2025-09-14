#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

def main():
    """Run administrative tasks."""
    # This assumes your settings file is at api/settings.py
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
    
    # --- FIX ---
    # Add the project root directory (the parent of the 'api' directory)
    # to the Python path. This allows Python to find the 'apps' module.
    # This should be the path to your 'stories-service' directory.
    project_root = Path(__file__).resolve().parent.parent
    sys.path.append(str(project_root))
    # --- END FIX ---

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
