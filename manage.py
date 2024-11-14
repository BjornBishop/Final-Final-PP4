#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_path)  # Added this line
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sagacity.config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()