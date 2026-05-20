# We import path from django.urls to register specific URL routes for our gallery views.
from django.urls import path
# We import our local views module to connect paths to our view functions.
from . import views

# ==============================================================================
# REAL-WORLD ANALOGY: The Exhibition Hall Signposts
# ------------------------------------------------------------------------------
# In Task 1, we likened our Django project to a grand shopping mall. 
# Inside the mall, we just opened a new custom wing called the "Gallery App".
# 
# Creating this local `gallery/urls.py` file is like putting up a clean directory 
# board at the entrance of our gallery wing. 
# 
# When a shopper walks straight into our empty root path (''), this directory 
# board immediately points them to our curator's front desk (`views.gallery_view`)
# and gives the path the official nickname 'index'.
# ==============================================================================

# We define the list of URL patterns that are active inside our gallery app.
urlpatterns = [
    # We map the root path '' directly to our gallery_view.
    # By passing the empty string, this view will load when someone visits http://127.0.0.1:8000/
    # We name the route 'index' so that all other views and templates can link back here easily.
    path('', views.gallery_view, name='index'),

    # ==========================================================================
    # REAL-WORLD ANALOGY: The Catalog Spotlight Door Number (Dynamic URL Path)
    # --------------------------------------------------------------------------
    # Imagine you want to give each photographic print its own dedicated viewing room.
    # Instead of building 1,000 separate rooms and painting 1,000 different signs (hardcoded URLs),
    # you build one magic room called "Photo Spotlight" and put a sliding slot on the door.
    #
    # When a visitor wants to view photo #12, they look at the directory sign: "photo/12/".
    # The URL router:
    # 1. Matches the "photo/" prefix.
    # 2. Extracts the number "12" from the sliding slot because it fits the <int:photo_id> rule.
    # 3. Securely locks the integer value "12" inside a variable named 'photo_id'.
    # 4. Guides the visitor and variable straight to the curator's photo_detail_view desk!
    # ==========================================================================
    
    # We map the URL path 'photo/<int:photo_id>/' to our photo_detail_view function.
    # <int:photo_id>: A path converter that matches any positive integer and saves it under the variable 'photo_id'.
    # name='photo_detail': The official nickname of this path, allowing us to do dynamic reverse lookup in templates.
    path('photo/<int:photo_id>/', views.photo_detail_view, name='photo_detail'),

    # ==========================================================================
    # REAL-WORLD ANALOGY: The Album Builder Desk (Creation Route)
    # --------------------------------------------------------------------------
    # When an artist wants to request a brand new empty binder, they walk up 
    # to the registration desk labeled "album/new/". 
    # This desk registers their request and directs them to the view where 
    # the paper form is waiting to be filled.
    # ==========================================================================
    path('album/new/', views.album_create_view, name='album_create'),

    # ==========================================================================
    # REAL-WORLD ANALOGY: The Album Display Room Binders (Dynamic Album Detail Route)
    # --------------------------------------------------------------------------
    # Just like each photograph, each album has its own unique showcase room 
    # with a dynamic ticket slot: "album/1/", "album/2/".
    # Django extracts the database record integer from the <int:album_id> slot
    # and routes it directly to the curator's album_detail_view function.
    # ==========================================================================
    path('album/<int:album_id>/', views.album_detail_view, name='album_detail'),

    # ==========================================================================
    # REAL-WORLD ANALOGY: The Photo Mounting Desk (Photo Upload Route)
    # --------------------------------------------------------------------------
    # When a photographer brings a new visual master print to the studio, they
    # carry it to the registration desk labeled "photo/upload/".
    # This desk welcomes them, verifies their credentials, and displays the
    # visual upload template to mount and save their picture file.
    # ==========================================================================
    path('photo/upload/', views.upload_photo_view, name='photo_upload'),
]

