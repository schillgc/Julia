"""
This file demonstrates two ways of documenting a Python module.
The first way is to use docstrings, which are strings that occur as the first statement in a module, function, class, or method definition. They are not executed as code, but are used by documentation generators like Sphinx to create API documentation.
The second way is to use a special comment called a type hint, which is a way to tell the Python interpreter what kind of data a variable or function returns. This can be useful for code completion and static analysis tools.
In this file, we import the django.contrib.admin module and register the Career model with the admin site.
"""

from django.contrib import admin

from .models import Career

"""
This function registers the Career model with the Django admin site.

Args:
    model (Model): The model to be registered with the Django admin site.

Returns:
    None
"""

admin.site.register(Career)
"""
Registers the Career model with the Django admin site.

Args:
    model (Model): The model to be registered with the Django admin site.

Returns:
    None
"""
pass
