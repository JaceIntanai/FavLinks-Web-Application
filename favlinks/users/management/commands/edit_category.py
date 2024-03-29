from django.core.management.base import BaseCommand, CommandError
from users.models import Categorie


class Command(BaseCommand):
    help = "Edit category"

    def add_arguments(self, parser):
        parser.add_argument("old_cate_name", type=str, help='old category name')
        parser.add_argument("new_cate_name", type=str, help='fill new category name')

    def handle(self, *args, **options):
        old_cate_name = options["old_cate_name"]
        new_cate_name = options["new_cate_name"]
        try:
            cate = Categorie.objects.get(cate_name=old_cate_name)
            cate.update(cate_name=new_cate_name)
            cate.save()
        except :
            raise CommandError(f'Category "{old_cate_name}" edit failed')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully edited from "{old_cate_name}" to "{new_cate_name}"')
        )