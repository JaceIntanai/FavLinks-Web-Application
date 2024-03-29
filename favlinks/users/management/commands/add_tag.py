from django.core.management.base import BaseCommand, CommandError
from users.models import Tag


class Command(BaseCommand):
    help = "Add new tag"

    def add_arguments(self, parser):
        parser.add_argument("tag_name", type=str, help='fill new tag name')

    def handle(self, *args, **options):
        tag_name = options["tag_name"]
        try:
            tag = Tag.objects.create(tag_name=tag_name)
            tag.save()
        except :
            raise CommandError(f'Tag "{tag_name}" create failed')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created "{tag_name}"')
        )