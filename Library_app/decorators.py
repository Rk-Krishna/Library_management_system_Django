from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
 
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('dashboard'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'student'):
            return HttpResponseRedirect(reverse('login'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'staff'):
            return HttpResponseRedirect(reverse('login'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view
