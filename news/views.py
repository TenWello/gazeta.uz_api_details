from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from news.fetch_gazetauz import get_gazeta_uz_latest_links, get_gazeta_uz_details
from news.models import GazetaNews
import time

class GazetaNewsBatchDetailApi(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        # 1) DB’dan: agar oldindan fetch_qazetauz bilan to‘ldirilgan bo‘lsa
        qs = GazetaNews.objects.exclude(title="").values(
            "title", "link", "time_ago", "full_text", "images"
        )
        return Response({"result": list(qs)}, status=status.HTTP_200_OK)

    def post(self, request):
        # 2) yoki POST qilinsa, body.links bo‘yicha real-time fetch
        links = request.data.get("links")
        if not isinstance(links, list) or not links:
            return Response({"error": "links list required"}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        for link in links:
            data = get_gazeta_uz_details(link)
            GazetaNews.objects.update_or_create(link=link, defaults=data)
            results.append(data)
            time.sleep(1)
        return Response({"result": results}, status=status.HTTP_200_OK)
