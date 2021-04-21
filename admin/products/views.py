"""Products Views"""

# Django REST Framework
from rest_framework import viewsets, status, exceptions, views
from rest_framework.response import Response

# Models
from products.models import Product, User

# Serializers
from products.serializers import ProductsSerializer

# Utils
import random


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)

        return Response(serializer.data)

    def create(self, request):
        serializer = ProductsSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise exceptions.NotFound()

        serializer = ProductsSerializer(product)

        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise exceptions.NotFound()

        serializer = ProductsSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            raise exceptions.NotFound()

        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(views.APIView):
    def get(self, _):
        users = User.objects.all()

        if len(users) > 0:
            user = random.choice(users)
        else:
            raise exceptions.NotFound()

        return Response({'id': user.id})
