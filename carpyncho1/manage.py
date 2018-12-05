#!/usr/bin/env python

def run_manager():
    import os
    import sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carpyncho.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    run_manager()
