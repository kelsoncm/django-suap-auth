#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv
from pathlib import Path


def main():
    # Load .env file before Django initialization
    env_file = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_file)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
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
