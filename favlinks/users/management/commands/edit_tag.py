from django.core.management.base import BaseCommand, CommandError
from users.models import Tag


class Command(BaseCommand):
    help = "Edit tag"

    def add_arguments(self, parser):
        parser.add_argument("old_tag_name", type=str, help='old tag name')
        parser.add_argument("new_tag_name", type=str, help='fill new tag name')

    def handle(self, *args, **options):
        old_tag_name = options["old_tag_name"]
        new_tag_name = options["new_tag_name"]
        try:
            tag = Tag.objects.get(tag_name=old_tag_name)
            tag.update(tag_name=new_tag_name)
            tag.save()
        except :
            raise CommandError(f'Tag "{old_tag_name}" edit failed')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully edited tag name from "{old_tag_name}" to "{new_tag_name}"')
        )