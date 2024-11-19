from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class adminAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated. and is an admin"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect("Library_app:dashboard")
        return super().dispatch(request, *args, **kwargs)
