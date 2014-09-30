from models import AllowedReferrer

class CORSMiddleware(object):
    def process_response(self, request, response):
        if 'key' in request.GET:
            referrers = AllowedReferrer.objects.filter(
                                project__api_key=request.GET.get('key'))\
                            .values_list('url', flat=True)
            if referrers:
                response['Access-Control-Allow-Origin'] = ','.join(referrers)
        return response
