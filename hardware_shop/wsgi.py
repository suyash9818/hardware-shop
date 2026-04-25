import os
import logging

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hardware_shop.settings')
application = get_wsgi_application()


def run_startup_migrations():
    if os.getenv("DJANGO_MIGRATE_ON_STARTUP", "1") != "1":
        return

    try:
        call_command("migrate", interactive=False, verbosity=0)
    except Exception:
        logging.getLogger(__name__).exception("Startup migrations failed.")
        raise


run_startup_migrations()
