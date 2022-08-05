from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from ian_account.models import User
from ian_auth.models import AnonymousIANYusa, MiddlewareIANUser


def get_user(request) -> User:
    """
    Get User obj.

    Returns an AnonymousIANYusa obj, or a accounts.models.User obj
    """
    yusa = AnonymousIANYusa()
    ian_user: MiddlewareIANUser = request.ian_user
    request_user = request.user
    if ian_user.is_anonymous and request_user.is_anonymous:
        return yusa
    if ian_user.is_anonymous and not request_user.is_anonymous:
        try:
            user: User = User.objects.get(email=request_user.email)
        except User.DoesNotExist:
            return yusa

    if not ian_user.is_anonymous:
        try:
            user: User = User.objects.get(email=ian_user.email)
        except User.DoesNotExist:
            return yusa  
    if user.token == ian_user.auth:
        return user
    return yusa



class ExpenslyYusaAuthenticationMiddleware(MiddlewareMixin):
    """
    Inject yusa object to request

    TODO - Add request.merchant and request.merchant_user for merchants.
    """

    def process_request(self, request):
        assert hasattr(
            request, "ian_user"
        ), "Expensly requires that you add ian_auth.middleware.IANAuthMiddleware to your MIDDLEWARE section on your settings."
        request.yusa = SimpleLazyObject(lambda: get_user(request))
       
