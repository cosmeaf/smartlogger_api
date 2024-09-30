from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.management import color

class Command(BaseCommand):
    help = 'Create a new user with the specified username, password, and optional details.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='The username for the new user')
        parser.add_argument('--password', required=True, help='The password for the new user')
        parser.add_argument('--email', help='The email address for the new user')
        parser.add_argument('--first_name', help='The first name of the new user')
        parser.add_argument('--last_name', help='The last name of the new user')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        email = kwargs.get('email')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"Error: A user with the username '{username}' already exists."))
            return

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully created user '{username}'."))

    def usage(self, subcommand):
        usage_text = f"""
Usage: python manage.py {subcommand} --username=<username> --password=<password> [options]

Options:
  --username     The username for the new user (required)
  --password     The password for the new user (required)
  --email        The email address for the new user (optional)
  --first_name   The first name of the new user (optional)
  --last_name    The last name of the new user (optional)
  --help         Show this message and exit

Examples:
  python manage.py {subcommand} --username=johndoe --password=secret123
  python manage.py {subcommand} --username=johndoe --password=secret123 --email=johndoe@example.com

Warning:
  Please make sure to choose a strong password.
"""
        return usage_text

    def print_help(self, *args, **kwargs):
        style = color.color_style()
        help_text = self.help
        self.stdout.write(style.NOTICE(help_text))
        self.stdout.write(self.usage('createuser'))
