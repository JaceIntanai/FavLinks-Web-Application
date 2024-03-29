from django.core.management.base import BaseCommand, CommandError
from users.models import Tag, URL, Categorie
from users.independence import validate_url
from django.utils import timezone

class Command(BaseCommand):
    help = "Edit URL"

    def add_arguments(self, parser):
        parser.add_argument("old_title_name", type=str, help='old title name')
        parser.add_argument("new_title_name", type=str, help='fill new title name')
        parser.add_argument("old_url", type=str, help='old link url')
        parser.add_argument("new_url", type=str, help='fill new link url')
        parser.add_argument("categories", type=list, help='fill list of categories')
        parser.add_argument("tags", type=list, help='fill list of tags')

    def handle(self, *args, **options):
        old_title_name = options["old_title_name"]
        new_title_name = options["new_title_name"]
        old_url = options["old_url"]
        new_url = options["new_url"]
        categories = options["categories"]
        tags = options["tags"]

        try:
            select_url = URL.objects.get(title_name=old_title_name, url=old_url)
            select_url.update(
                title = new_title_name,
                url = new_url,
                validate_url = validate_url(new_url),
                url_check_dtm = timezone.now(),
            )
            for category in categories:
                try:
                    cate = Categorie.objects.get(cate_name = category)
                except:
                    raise CommandError(f'Category name "{category}" not in database')
                select_url.add(categories = cate)
            for tag in tags:
                try:
                    tag_select = Tag.objects.get(tag_name = tag)
                except:
                    raise CommandError(f'Tag name "{tag_select}" not in database')
                select_url.add(tags = tag_select)
            select_url.save()
        except :
            raise CommandError('URL edit failed')

        self.stdout.write(
            self.style.SUCCESS('Successfully edited URL')
        )