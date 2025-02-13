class RequestLogMiddleware:
    """
    Middleware, które loguje każde przychodzące żądanie.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"🔎 Request: {request.method} {request.get_full_path()}")
        response = self.get_response(request)
        print(f"🔎 Response status: {response.status_code}")
        return response
