# We import the core models library from Django to build database blueprints.
from django.db import models
# We import settings to reference our custom User model in a modular, flexible way.
# Analogy: Instead of hardcoding a specific brand of battery into a device, we reference 
# the master blueprint's specifications so we can swap the battery brand without redesigning the device.
from django.conf import settings

# ==============================================================================
# REAL-WORLD ANALOGY: The Photo Album Organizer (Our Album Model)
# ------------------------------------------------------------------------------
# Imagine a physical photo binder with a user's name tag on the front cover. 
# The binder has:
# 1. A neat label identifying who owns it (user ForeignKey).
# 2. A title on the spine (e.g., "Summer Vacation 2026").
# 3. A written description inside the cover describing the photos inside.
#
# Our `Album` class is the digital blueprint for this physical photo binder.
# ==============================================================================

# We define the Album model, which creates a corresponding table in our database.
class Album(models.Model):
    # A relationship mapping this album to the specific User who created it.
    # settings.AUTH_USER_MODEL points to our custom 'accounts.User' model.
    # on_delete=models.CASCADE tells Django: "If this user deletes their account,
    # immediately shred and delete all of their photo albums too so no ghost data is left!"
    # related_name='albums' lets us easily look up all albums belonging to a user (e.g., user.albums.all()).
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='albums'
    )
    
    # A character field for the album's name. We set a maximum capacity of 200 characters.
    # Analogy: This is the label slot on the spine of the physical binder.
    title = models.CharField(max_length=200)
    
    # A large text area for a detailed description of the album.
    # blank=True means this field is completely optional; users don't have to fill it in.
    # Analogy: This is an optional notebook page inside the cover where users can jot down a story.
    description = models.TextField(blank=True)
    
    # A date and time stamp that is automatically set when the album is first created.
    # auto_now_add=True records the exact microsecond the album is saved to the database.
    # Analogy: The factory prints the manufacturing date on the back of the album cover automatically.
    created_at = models.DateTimeField(auto_now_add=True)

    # The __str__ method tells Python how to represent this object as a simple text string.
    # Analogy: When the librarian asks, "What album is this?", we read out the title instead of a cold ID number.
    def __str__(self):
        # We return the album's title string.
        return self.title


# ==============================================================================
# REAL-WORLD ANALOGY: The Individual Photograph (Our Photo Model)
# ------------------------------------------------------------------------------
# Imagine a physical photo printout. On the back of the printout:
# 1. We write a caption title (title).
# 2. We stick it inside a specific binder (album ForeignKey).
# 3. The actual picture image itself is saved on a physical paper canvas (image field).
#
# Our `Photo` class is the digital blueprint for each physical photograph print.
# ==============================================================================

# We define the Photo model, creating a database table for individual pictures.
class Photo(models.Model):
    # A relationship mapping this photo to a parent Album binder.
    # on_delete=models.CASCADE tells Django: "If this album binder is thrown away,
    # immediately throw away and shred all the individual photographs that were inside it!"
    # related_name='photos' lets us retrieve all photos inside an album easily (e.g., album.photos.all()).
    album = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    
    # A character field for the photo's caption or title, capped at 200 characters.
    title = models.CharField(max_length=200)
    
    # A specialized image upload field.
    # upload_to='photos/' tells Django: "When saving this physical file on the hard drive,
    # place it inside a subfolder named 'photos' under the main MEDIA_ROOT warehouse folder."
    # Django's ImageField automatically performs security checks to ensure the file is a valid image.
    image = models.ImageField(upload_to='photos/')
    
    # A timestamp automatically set when the photo is uploaded.
    # Analogy: A digital camera prints the date and time in orange text on the corner of the picture.
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Represents the Photo object as a text string (e.g., in the admin dashboard).
    # Analogy: Reading out the photo's caption instead of showing a random database row index.
    def __str__(self):
        # We return the photo's title string.
        return self.title
