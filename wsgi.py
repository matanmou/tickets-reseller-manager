"""
WSGI entry point for Apache mod_wsgi.

Apache loads `application` from this module — see apache/tickets-reseller.conf.
For local development, run:  FLASK_APP=wsgi:application flask run
"""

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from app import create_app

application = create_app()
