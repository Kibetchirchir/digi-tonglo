from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoadWalletSerializer
 
class LoadWalletAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoadWalletSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data = serializer.data, status=status.HTTP_201_CREATED)