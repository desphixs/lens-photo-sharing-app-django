# We import standard Django utilities for handling view logic.
# render: used to load and send HTML templates (like gallery.html) back to the browser.
# get_object_or_404: used to fetch a single record from the database, or immediately return a 404 error if it doesn't exist.
# redirect: used to route a user's browser dynamically to another URL or named view.
from django.shortcuts import render, get_object_or_404, redirect
# We import login_required decorator to protect secure creation pages.
from django.contrib.auth.decorators import login_required
# We import our custom Album and Photo blueprints to fetch data from the database.
from gallery.models import Album, Photo
# We import our custom AlbumForm and PhotoForm to process and validate user input.
from gallery.forms import AlbumForm, PhotoForm

# ==============================================================================
# REAL-WORLD ANALOGY: The Art Gallery Curator
# ------------------------------------------------------------------------------
# Imagine you are the curator of a premium physical art gallery. 
# Before the grand opening doors swing open for the public:
# 1. You walk back into the storage vaults (database).
# 2. You gather all the beautiful wooden display stands (Album records).
# 3. You retrieve every single framed photographic canvas print (Photo records).
# 4. You arrange the stands in a neat row and mount the canvases elegantly.
# 5. You open the gallery doors and welcome visitors to view the exhibition (render gallery.html).
# ==============================================================================

# We define the view function that handles our public homepage portfolio.
def gallery_view(request):
    # ---- STEP 1: Fetch all Albums ----
    # We query the database to retrieve all registered Album objects.
    # .order_by('-created_at') sorts them so the newest album binders show up first.
    # Analogy: Grabbing all the display stands and sorting them from newest to oldest.
    albums = Album.objects.all().order_by('-created_at')
    
    # ---- STEP 2: Fetch all Photos ----
    # We query the database to retrieve all uploaded Photo objects.
    # .order_by('-uploaded_at') sorts the photos so Casey's latest photography is displayed first.
    # Analogy: Gathering all the photographic prints and ordering them by date.
    photos = Photo.objects.all().order_by('-uploaded_at')
    
    # ---- STEP 3: Render and Deliver the Gallery ----
    # We call render to load our 'gallery.html' template and inject our database lists.
    # The third argument is the context dictionary, which acts as our courier box.
    # It carries our Python lists ('albums' and 'photos') straight into the HTML file.
    return render(request, 'gallery.html', {
        'albums': albums,
        'photos': photos,
    })


# ==============================================================================
# REAL-WORLD ANALOGY: The Solo Exhibition Spotlight (Our Photo Detail View)
# ------------------------------------------------------------------------------
# Imagine a guest walks into the gallery and sees a stunning postcard capture in the grid.
# They point to it and ask the curator: "I want to see this specific picture under the
# high-magnification spotlight in a private viewing room, along with its full details!"
#
# The curator:
# 1. Takes the unique catalog index number of the photo (the photo_id).
# 2. Walks into the secure vault storage files (database).
# 3. Searches for that exact catalog record (using get_object_or_404).
#    - If it's found, the curator carries it to the private room.
#    - If someone made up a random index number that doesn't exist, the bouncer 
#      immediately steps in and politely turns them away (returns a 404 page).
# 4. Sets up the private spotlight viewing screen (renders photo_detail.html)
#    and passes the single dynamic Photo canvas directly to the spotlight room!
# ==============================================================================

# We define the view function that displays a single, detailed view of a photograph.
# Django automatically passes the 'pk' parameter matched from our URL as 'photo_id'.
def photo_detail_view(request, photo_id):
    # ---- STEP 1: Retrieve the Specific Photo or Fail Gracefully ----
    # We query our Photo model to find the single record whose unique ID matches 'photo_id'.
    # get_object_or_404 takes the model class and the lookup parameter.
    # Analogy: Sending the vault assistant to grab one specific print catalog number.
    photo = get_object_or_404(Photo, pk=photo_id)

    # ---- STEP 2: Render and Deliver the Spotlight Template ----
    # We load our clean spotlight template named 'photo_detail.html'.
    # We pack our retrieved single photo object into the courier context dictionary.
    # Analogy: Bringing the single canvas and mounting it in the dark spotlight room.
    return render(request, 'photo_detail.html', {
        'photo': photo, # This is the same thing as creating a context dictionary
    })


# ==============================================================================
# REAL-WORLD ANALOGY: The Album Builder Workshop (Our Album Creation View)
# ------------------------------------------------------------------------------
# Imagine you are in a woodcraft studio and want to build a brand new physical photo binder.
# 1. You walk up to the supervisor's desk (The Server).
# 2. If you are a guest, the supervisor stops you at the gate and directs you to sign in 
#    first (using `@login_required` badge checker).
# 3. Once inside, if you are just browsing (GET request), the supervisor hands you a 
#    fresh, blank paper application form (AlbumForm) to write down your binder details.
# 4. If you have finished writing and hit submit (POST request), the supervisor:
#    a. Grabs your paper application sheet.
#    b. Runs checks to make sure you didn't leave critical fields blank (form validation).
#    c. Attaches your official badge name onto the binder's ownership tag (album.user = request.user).
#    d. Saves it securely in the cabinet shelf (album.save()).
#    e. Guides you straight to the newly made binder detail room (redirect to album_detail)!
# ==============================================================================

# We protect this view so only logged-in users can access the creation workshop room.
@login_required
def album_create_view(request):
    # ---- STEP 1: Check request method ----
    # If the user submitted form entries (POST), we process the data.
    # If they just clicked a link to view the page (GET), we skip to showing a blank form.
    if request.method == 'POST':
        # We initialize our AlbumForm filled with the user's raw POST submissions.
        # Analogy: Writing down their submitted answers onto our structured form blueprint.
        form = AlbumForm(request.POST)
        
        # We validate the submitted details against models character limits and rules.
        if form.is_valid():
            # We save the form to build our new Album instance, but pause saving to the database.
            # commit=False lets us modify fields manually before writing records to sqlite.
            # Analogy: Holding the binder in our hands before stamping it with the official database ID.
            album = form.save(commit=False)
            
            # We link this album to the currently authenticated User account.
            # Analogy: Writing the active photographer's badge ID on the owner tag.
            album.user = request.user
            
            # We save the fully detailed Album record securely into our database table.
            # Analogy: Sliding the finished physical binder onto the vault showcase shelves.
            album.save()
            
            # We dynamically redirect the user straight to the new album showcase page.
            # Analogy: Guiding the artist and their guests directly into their brand new album room.
            return redirect('album_detail', album_id=album.id)
    else:
        # If it's a GET request, we present a fresh, blank form.
        # Analogy: Handing the artist a clean, empty paper sheet to fill in.
        form = AlbumForm()
        
    # We load our creation form template, passing the form in the context courier box.
    # Analogy: Opening the workshop studio page and presenting the paper form.
    return render(request, 'album_create.html', {
        'form': form,
    })


# ==============================================================================
# REAL-WORLD ANALOGY: The Album Showroom Binders (Our Album Detail View)
# ------------------------------------------------------------------------------
# Imagine a visitor walks into our gallery portfolio showroom and sees a premium wooden display binder.
# They pull it from the rack and ask the curator to open it: "Show me all the photos inside!"
#
# The curator:
# 1. Takes the unique catalog album number (album_id).
# 2. Searches for the specific binder shelf (using get_object_or_404).
#    - If it's not on the rack, they inform the visitor it's missing (returns 404).
# 3. Pulls out every single photograph print tucked inside that specific folder (album.photos.all()).
# 4. Sorts them neatly so the newest snapshots sit on the top page (order_by('-uploaded_at')).
# 5. Opens the binder page and lays out the photographs beautifully on the desk (renders album_detail.html).
# ==============================================================================

# We define the view function that displays a single album and all of its associated photo grid elements.
def album_detail_view(request, album_id):
    # ---- STEP 1: Fetch the Specific Album or return 404 ----
    # We query our Album table to find the single record whose unique ID matches 'album_id'.
    # get_object_or_404 takes the model class and the lookup primary key.
    # Analogy: Grabbing one specific catalog binder block by its registered identifier.
    album = get_object_or_404(Album, pk=album_id)
    
    # ---- STEP 2: Fetch all Photos in this specific Album ----
    # We utilize Django's related manager (album.photos.all()) to retrieve all photos pointing to this album.
    # We order them by upload time so Casey's latest photography work shows up first.
    # Analogy: Spreading all photographs out in chronological order.
    photos = album.photos.all().order_by('-uploaded_at')
    
    # ---- STEP 3: Render and Deliver the Showroom Template ----
    # We call render to load our 'album_detail.html' template and inject our album and photos lists.
    # Analogy: Lying the open binder out on the glass viewing table in our premium spotlight suite.
    return render(request, 'album_detail.html', {
        'album': album,
        'photos': photos,
    })


# ==============================================================================
# REAL-WORLD ANALOGY: The Art Studio Upload Desk (Our Photo Upload View)
# ------------------------------------------------------------------------------
# Imagine you are a photographer standing in front of a busy art studio.
# You have a fresh, glossy photograph print (the image file) sitting in your handbag.
# Before you can place it inside one of the gallery's display binders:
# 1. The security guard checks your membership badge at the gate to ensure you are logged in
#    (using the `@login_required` security bouncer).
# 2. If you are just visiting the room (GET request), the desk clerk hands you a 
#    pre-printed physical submission card (PhotoForm) that asks:
#    - "Which of your binders do you want to add this print to?"
#    - "What caption title do you want to give this picture?"
#    - "Where is the physical photo print file?"
# 3. If you have filled out the card, attached the physical image print, and hit submit (POST request), the clerk:
#    a. Grabs the filled-out form data and retrieves the physical print file from your handbag
#       (using the special `request.FILES` dictionary).
#    b. Packs these into the form validation machine to verify that the file is actually a clean, valid image
#       and the title is within character limit constraints.
#    c. Saves the new photograph securely into the database vault (photo.save()).
#    d. Guides you straight into the dynamic album showcase detail room to view your newly mounted picture!
# ==============================================================================

# We protect this view so only logged-in users can upload and add photos to the studio gallery.
@login_required
def upload_photo_view(request):
    # ---- STEP 1: Check request method ----
    # If the user submitted form inputs and physical files (POST), we process the submission.
    # If they are just landing on the upload page (GET), we present them a clean, empty form.
    if request.method == 'POST':
        # We initialize our PhotoForm filled with user text entries (request.POST) AND physical files (request.FILES).
        # We pass the authenticated 'user' parameter so the form choice list is dynamically filtered to only their albums.
        # Analogy: Filling out the paper slip and pulling the physical photograph out of the visitor's handbag.
        form = PhotoForm(request.POST, request.FILES, user=request.user)
        
        # We validate the submitted fields against models character limits and file requirements.
        if form.is_valid():
            # We save the form directly to write and record our new Photo object in the database.
            # Unlike the album, the user selects the album directly from the dropdown, so all relationships are defined.
            # Analogy: Committing the new photo print to the database cabinet and copying the file to storage.
            photo = form.save()
            
            # We dynamically redirect the user straight to the album detail page of the album they selected.
            # Analogy: Guiding the artist directly to the folder where their new capture is proudly hanging.
            return redirect('album_detail', album_id=photo.album.id)
    else:
        # If it's a GET request, we present a fresh, blank form.
        # We pass the active 'user' keyword parameter to restrict album list options to only their albums.
        # Analogy: Handing the visitor a clean, empty submission sheet with a dropdown of only their folders.
        form = PhotoForm(user=request.user)
        
    # We load our upload form template, passing the styled form blueprint in the context courier box.
    # Analogy: Welcoming the artist to the upload studio workshop table and laying out the form fields.
    return render(request, 'upload.html', {
        'form': form,
    })


