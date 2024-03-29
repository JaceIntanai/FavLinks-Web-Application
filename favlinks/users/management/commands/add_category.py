from django.core.management.base import BaseCommand, CommandError
from users.models import Categorie


class Command(BaseCommand):
    help = "Add new category"

    def add_arguments(self, parser):
        parser.add_argument("cate_name", type=str, help='fill new category name')

    def handle(self, *args, **options):
        cate_name = options["cate_name"]
        try:
            cate = Categorie.objects.create(cate_name=cate_name)
            cate.save()
        except :
            raise CommandError(f'Category "{cate_name}" create failed')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created "{cate_name}"')
        )