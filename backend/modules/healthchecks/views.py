from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class HealthCheckApiView(GenericAPIView):
    permission_classes = []

    def get(self, *args, **kwargs):
        return Response({"message": "email-reader app works!"})
