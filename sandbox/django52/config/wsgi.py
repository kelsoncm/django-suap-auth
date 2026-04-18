import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file before Django initialization
env_file = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_file)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
