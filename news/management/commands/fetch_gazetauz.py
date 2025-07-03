from django.core.management.base import BaseCommand
from news.models import GazetaNews
from news.fetch_gazetauz import get_gazeta_uz_latest_links, get_gazeta_uz_details
import time

class Command(BaseCommand):
    help = "Fetch latest Gazeta.uz news + details into DB"

    def handle(self, *args, **options):
        links = get_gazeta_uz_latest_links(limit=30)
        self.stdout.write(f"{len(links)} ta yangilik topildi. Boshlanmoqda…")

        for i, link in enumerate(links, start=1):
            data = get_gazeta_uz_details(link)
            GazetaNews.objects.update_or_create(link=link, defaults=data)
            self.stdout.write(self.style.SUCCESS(f"{i}/{len(links)} • {data['title']}"))
            time.sleep(1)

        self.stdout.write(self.style.SUCCESS("BARCHA YANGILIKLAR SAQLANDI!"))