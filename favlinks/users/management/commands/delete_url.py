from django.core.management.base import BaseCommand, CommandError
from users.models import Tag, URL, Categorie
from users.independence import validate_url

class Command(BaseCommand):
    help = "Delete URL"

    def add_arguments(self, parser):
        parser.add_argument("title_name", type=str, help='fill title name')
        parser.add_argument("url", type=str, help='fill link url')

    def handle(self, *args, **options):
        title_name = options["title_name"]
        url = options["url"]

        try:
            new_url = URL.objects.get(title_name=title_name, url=url)
            new_url.delete()
        except :
            raise CommandError('URL delete failed')

        self.stdout.write(
            self.style.SUCCESS('Successfully deleted URL')
        )