from rest_framework import mixins, viewsets


class ModelCVDViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`,
    `destroy()` and `list()` actions.
    """
    pass
