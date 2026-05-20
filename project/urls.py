"""
URL configuration for authify_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# We import path and include from django.urls.
# path: used to define exact web address routes.
# include: used to reference other local app urls.py files, keeping routing modular.
from django.urls import path, include
# We import the admin module to route to Django's built-in administration site.
from django.contrib import admin
# We import settings so we can access variables defined in settings.py (like DEBUG, MEDIA_URL, and MEDIA_ROOT).
# Analogy: This is like referencing the master handbook so we know if the building is under construction or open to the public.
from django.conf import settings
# We import static to generate the URL pattern mappings that tell Django how to serve files during development.
# Analogy: This is like calling a temporary tour guide service that only operates while the building is under construction.
from django.conf.urls.static import static

# ==============================================================================
# REAL-WORLD ANALOGY: The Central Information Desk
# ------------------------------------------------------------------------------
# Imagine the main `urls.py` is the chief receptionist standing at the front door 
# of the Django tower. 
# 
# When a visitor walks in and asks to visit "/admin/", the chief receptionist 
# handles it directly by pointing them to Django's built-in admin room.
# 
# But when a visitor asks for anything else (like "/register/"), the receptionist
# doesn't know every single private desk layout. Instead, they look at the rule:
# `path('', include('accounts.urls'))`
# 
# This rule tells the receptionist: "For any standard site traffic, hand the visitor's
# map over to the Accounts Department receptionist (accounts.urls) and let them guide
# the visitor to the final desk!"
# ==============================================================================

# We define the master list of URL paths for the entire website.
urlpatterns = [
    # Routes any requests starting with 'admin/' directly to the Django Admin backend.
    path('admin/', admin.site.urls),
    # We include our accounts app urls.py. By passing an empty string '' as the prefix,
    # we allow routes defined in accounts/urls.py (like 'register/') to be accessed
    # directly at the root level (e.g., 'http://127.0.0.1:8000/register/').
    path('', include('accounts.urls')),
]

# ==============================================================================
# REAL-WORLD ANALOGY: The Temporary Tour Guide for Media Files
# ------------------------------------------------------------------------------
# In a large production web application, you would never ask your core Python server (Django)
# to serve heavy image files to users. It would get bogged down and slow to a crawl!
# Instead, you would hire a professional digital courier service (like Amazon Web Services S3,
# Nginx, or Cloudflare) to serve your images at lightning speed.
# 
# However, while we are building and testing our app locally (where settings.DEBUG is True),
# we don't have Nginx or AWS S3 set up on our personal computer.
# 
# Adding the `static(...)` helper at the bottom is like giving our chief receptionist
# a temporary map extension: "If we are in test/debug mode, whenever a visitor comes asking
# for a picture file located at our shop display window path (settings.MEDIA_URL),
# guide them directly to the corresponding shelf in our storage warehouse (settings.MEDIA_ROOT)
# so they can see their beautiful photograph!"
# ==============================================================================

# We only want to serve media files directly from the development server during active local development (when DEBUG is True).
if settings.DEBUG:
    # We append the media-serving URL configurations to our master urlpatterns list.
    # static() takes the public web address prefix and the physical file directory path,
    # and generates a dynamic URL route that binds them together.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
