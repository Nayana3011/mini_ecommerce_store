import time


class RequestTimingMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        start_time = time.time()

        response = self.get_response(request)

        duration = (
            time.time() - start_time
        ) * 1000

        print(
            f"{request.method} "
            f"{request.path} "
            f"{duration:.2f} ms"
        )

        return response