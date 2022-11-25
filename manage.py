#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confectioner_bot.settings')
import django
from django.conf import settings

if not settings.configured:
    django.setup()

import sys
from bot.management.commands.bot import cake_bot


def main():
    """Run administrative tasks."""
#    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'confectioner_bot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    cake_bot()

    execute_from_command_line(sys.argv)



if __name__ == '__main__':
    main()
