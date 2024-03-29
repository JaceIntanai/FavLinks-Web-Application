from django.utils import timezone
from .models import UserProfile, URL, Categorie, Tag
import requests

def validate_urls():
    urls = URL.objects.all()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    for url in urls:
        try:
            response = requests.get(url.url, headers=headers, timeout=(5, None))

            if response.status_code == 200:
                url.url_validate = True
                url.url_check_dtm = timezone.now()
                url.save()
            else:
                url.url_validate = False
                url.url_check_dtm = timezone.now()
                url.save()
        except Exception as e:
            url.url_validate = False
            url.url_check_dtm = timezone.now()
            url.save()
            pass

def validate_url(url:str) -> bool:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False