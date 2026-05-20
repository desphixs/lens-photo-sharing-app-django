# We import the built-in admin module from Django to customize our Admin dashboard.
from django.contrib import admin
# We import our custom Album and Photo blueprints from the current directory's models.py file.
# The '.' indicates we are importing from the same folder where admin.py lives.
from gallery.models import Album, Photo

# ==============================================================================
# REAL-WORLD ANALOGY: Registering Books in a Library's Main Catalog
# ------------------------------------------------------------------------------
# Imagine the Django Admin Panel is a digital library office, and Django's admin bouncers
# are sitting at the front desk. Even though we just designed two new bookshelves 
# (our Album and Photo models) in our warehouse, the front desk bouncers have absolutely
# no idea they exist! They will not display them in their lobby.
# 
# Registering our models here is like walkng up to the head librarian's desk and handing
# them the catalog cards for our new shelves: "Attention! Please add the 'Album' and 
# 'Photo' cards to the master library index so authorized administrators can view, 
# create, edit, and organize them from the main control panel!"
# ==============================================================================

# We register the Album model with the admin site.
# This makes the Album table fully manageable within the Django Admin dashboard lobby.
admin.site.register(Album)

# We register the Photo model with the admin site.
# This makes the Photo table fully manageable, allowing admins to upload images directly.
admin.site.register(Photo)
