from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    """
    Decorator to restrict access only to student accounts. Redirects to login page for others.
    Credit to Vitor Freitas:
    https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html
    :param function: None
    :param redirect_field_name: REDIRECT_FIELD_NAME
    :param login_url: 'login'
    :return: actual_decorator or actual_decorator(function)
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

