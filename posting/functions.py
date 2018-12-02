from django.urls import reverse


def get_token_headers(request):
    jwt_token = request.COOKIES.get('token')

    if jwt_token is None:
        return None

    headers = {'Authorization': 'Bearer ' + jwt_token}
    return headers


def get_view_full_url(request, view_name, args=None):
    url = request.build_absolute_uri(location=reverse(view_name, args=args))
    return url
