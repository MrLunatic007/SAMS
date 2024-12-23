from django.shortcuts import redirect

def role_required(role):
    """
    Custom decorator to restrict view access based on user role.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user has the required role
            if getattr(request.user, role, False):  # Checks the `is_student` or `is_teacher` flag
                return view_func(request, *args, **kwargs)
            # Redirect unauthorized users to a custom error page or the previous page
            return redirect('core:access_denied')
        return _wrapped_view
    return decorator
