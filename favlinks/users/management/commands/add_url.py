from django.core.management.base import BaseCommand, CommandError
from users.models import Tag, URL, Categorie
from users.independence import validate_url

class Command(BaseCommand):
    help = "Add new URL"

    def add_arguments(self, parser):
        parser.add_argument("title_name", type=str, help='fill title name')
        parser.add_argument("url", type=str, help='fill link url')
        parser.add_argument("categories", type=list, help='fill list of categories')
        parser.add_argument("tags", type=list, help='fill list of tags')

    def handle(self, *args, **options):
        title_name = options["title_name"]
        url = options["url"]
        categories = options["categories"]
        tags = options["tags"]

        try:
            new_url = URL.objects.create(title_name=title_name, url=url, validate_url=validate_url(url))
            for category in categories:
                try:
                    cate = Categorie.objects.get(cate_name = category)
                except:
                    raise CommandError(f'Category name "{category}" not in database')
                new_url.add(categories = cate)
            for tag in tags:
                try:
                    tag_select = Tag.objects.get(tag_name = tag)
                except:
                    raise CommandError(f'Tag name "{tag_select}" not in database')
                new_url.add(tags = tag_select)
            new_url.save()
        except :
            raise CommandError('URL create failed')

        self.stdout.write(
            self.style.SUCCESS('Successfully created URL')
        )