import os
import time
import traceback
import signal
import sys
from django.core.wsgi import get_wsgi_application

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(APP_PATH)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TOPC_MS.settings")

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
