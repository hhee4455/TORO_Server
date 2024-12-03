import os
import sys
from django.core.management import execute_from_command_line

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        execute_from_command_line(sys.argv)
    except Exception as exc:
        raise exc

if __name__ == '__main__':
    main()
