from django.core.management.base import BaseCommand, CommandError
from users.models import Tag


class Command(BaseCommand):
    help = "Delete tag"

    def add_arguments(self, parser):
        parser.add_argument("tag_name", type=str, help='fill tag name to delete')

    def handle(self, *args, **options):
        tag_name = options["tag_name"]
        try:
            tag = Tag.objects.get(tag_name=tag_name)
            tag.delete()
        except :
            raise CommandError(f'Tag "{tag_name}" delete failed')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted "{tag_name}"')
        )