from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.permissions import IsShmurdikOrStaffPermission
from account.serializers import LoginSerializer, UserSerializer


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """User model viewset with list, retrieve, update and destroy functionality."""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    lookup_field = "username"

    def get_permissions(self):
        # Append additional permission classes depends on the request action.
        permissions = super().get_permissions()

        if self.action == "list":
            return [IsShmurdikOrStaffPermission(), *permissions]

        if self.action == "create":
            return [AllowAny(),]
        
        if self.action in ["update", "partial_update", "delete"]:
            return [IsAdminUser(), *permissions]

        return permissions

    @action(
        methods=["POST"], detail=False,
        serializer_class=LoginSerializer,
        permission_classes=(AllowAny,),
    )
    def login(self, request, format=None):
        """Login functionality.
        
        Authenticate user by the given `username` and `password` fields.
        Returns:
            Response (200) with the token if the user authenticated
            successfully, response (401) with the authenticate error message
            otherwise.
        """

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.data.get("username"),
            password=serializer.data.get("password"),
        )

        if user:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)

            return Response(
                {"detail": _("User account is not active.")},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            
        return Response(
            {"detail": _("Unable to login with provided credentials.")},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @action(
        methods=["POST"], detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def logout(self, request, format=None):
        """Logout functionality.
        
        Returns:
            Response(200) with success logout message.
        """

        Token.objects.filter(user=request.user).delete()

        return Response(
            {"success": _("User logged out.")},
            status=status.HTTP_200_OK,
        )


class UserPersonalViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """User personal retrieve, update and destroy functionality.
    
    Overrides the `get_object` method, so user can manage the personal instance
    only.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
