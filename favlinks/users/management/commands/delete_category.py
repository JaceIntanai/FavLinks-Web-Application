from django.core.management.base import BaseCommand, CommandError
from users.models import Categorie


class Command(BaseCommand):
    help = "Delete category"

    def add_arguments(self, parser):
        parser.add_argument("cate_name", type=str, help='fill category name to delete')

    def handle(self, *args, **options):
        cate_name = options["cate_name"]
        try:
            cate = Categorie.objects.get(cate_name=cate_name)
            cate.delete()
        except :
            raise CommandError(f'Category "{cate_name}" delete failed')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted "{cate_name}"')
        )