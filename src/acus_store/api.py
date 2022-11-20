from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from acus_store.models import Category, PriceRecord, Product
from acus_store.serializers import CategorySerializer, PricesSerializer, ProductSerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)


class PriceViewSet(ReadOnlyModelViewSet):
    queryset = PriceRecord.objects.all()
    serializer_class = PricesSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request: Request, pk: int | None = None) -> Response:
        queryset = PriceRecord.objects.filter(product_id=pk)
        serializer = PricesSerializer(queryset, many=True)
        return Response(serializer.data)
