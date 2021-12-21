from django.http import HttpResponse
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework import permissions
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('brand', 'item')
    serializer_class = ProductSerializer
    permission_classes = [DRYPermissions, permissions.IsAuthenticated]


def get_permissions(self):
    if self.request.method == 'GET' or self.request.method == 'PUT':
        return [DRYPermissions(),]
    return []
