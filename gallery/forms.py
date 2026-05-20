# We import Django's forms module to build secure, structured HTML form handlers.
from django import forms
# We import our Album and Photo models to bind this form structure straight to the database table columns.
from gallery.models import Album, Photo

# ==============================================================================
# REAL-WORLD ANALOGY: The Form Standard Blueprint (Our Album Creation Form)
# ------------------------------------------------------------------------------
# Imagine you go to a physical photo shop to print and organize your pictures.
# The shop manager doesn't hand you a blank piece of paper and tell you to guess what info they need.
# Instead, they hand you a structured paper application form with neatly labeled slots:
# - [ Title of Album ]
# - [ Story / Description of Album ]
#
# This paper form ensures that you only write down what's needed, checks that you don't leave the title blank
# (validation), and makes sure your handwriting stays within the lines.
# In Django, `forms.ModelForm` is that exact pre-printed paper application! It looks at our 
# Album model blueprint and automatically sets up input text boxes with the correct character limit rules.
# ==============================================================================

class AlbumForm(forms.ModelForm):
    # We specify metadata about the form in the inner Meta class.
    class Meta:
        # We tell Django to base this form on the Album database model.
        model = Album
        # We specify which database columns should be shown as input boxes on the form.
        # We exclude the 'user' field because we will assign it automatically in the view logic.
        fields = ['title', 'description']
        
        # We add dynamic visual styling attributes (widgets) so the inputs render beautifully with Tailwind.
        # Analogy: This is like picking premium glassmorphic border lines and sleek typography for our paper form.
        widgets = {
            # TextInput represents a single-line input field for short text fields.
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900/40 border border-zinc-800/80 focus:border-zinc-700 focus:ring-1 focus:ring-zinc-700 text-white rounded-xl py-3 px-4 text-sm font-semibold transition duration-200 placeholder-zinc-600 focus:outline-none',
                'placeholder': 'e.g., Summer in Tokyo 2026'
            }),
            # Textarea represents a multi-line box for longer text fields like descriptions.
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-zinc-900/40 border border-zinc-800/80 focus:border-zinc-700 focus:ring-1 focus:ring-zinc-700 text-white rounded-xl py-3 px-4 text-sm font-light transition duration-200 placeholder-zinc-600 focus:outline-none h-32 resize-none',
                'placeholder': 'Describe the story behind this collection...'
            }),
        }


# ==============================================================================
# REAL-WORLD ANALOGY: The Structured Photo Submission Form (Our Photo Form)
# ------------------------------------------------------------------------------
# Imagine walking up to a photo framing desk in the gallery to mount a physical print.
# The framing clerk hands you a standardized mounting request form containing:
# 1. A dropdown select box reading [ Choose Target Binder Folder ].
# 2. A single-line text input slot reading [ Caption or Title of Picture ].
# 3. A physical spring clip slot to slide in your [ Photograph Print Canvas ].
#
# This secure form template is what our `PhotoForm` builds! It ensures:
# - The student must select exactly which of *their* albums the picture will go in.
# - The caption is supplied without containing malicious text characters.
# - The image is a valid photograph file rather than plain text or binary executable code.
# ==============================================================================

class PhotoForm(forms.ModelForm):
    # We define the PhotoForm class inheriting from forms.ModelForm to map fields straight to our database
    class Meta:
        # We tell Django to base this form layout on the Photo database model.
        model = Photo
        # We specify which fields should be exposed as HTML inputs on the user's browser.
        fields = ['album', 'title', 'image']
        
        # We add gorgeous visual styling attributes to make our inputs look clean and modern.
        widgets = {
            # Select represents a dropdown pick list for linking ForeignKeys.
            'album': forms.Select(attrs={
                'class': 'w-full bg-zinc-900/40 border border-zinc-800/80 focus:border-zinc-700 focus:ring-1 focus:ring-zinc-700 text-white rounded-xl py-3.5 px-4 text-sm font-semibold transition duration-200 focus:outline-none appearance-none',
            }),
            # TextInput represents a single-line input field for the photo caption title.
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900/40 border border-zinc-800/80 focus:border-zinc-700 focus:ring-1 focus:ring-zinc-700 text-white rounded-xl py-3.5 px-4 text-sm font-semibold transition duration-200 placeholder-zinc-600 focus:outline-none',
                'placeholder': 'e.g., Majestic Tokyo Tower at Night'
            }),
            # FileInput represents the file browser dialog trigger for dynamic uploads.
            # We style this with Tailwind's modern file input utilities (file: styling) for premium feel.
            'image': forms.FileInput(attrs={
                'class': 'w-full bg-zinc-900/40 border border-zinc-800/80 focus:border-zinc-700 focus:ring-1 focus:ring-zinc-700 text-white rounded-xl py-3 px-4 text-sm font-semibold transition duration-200 focus:outline-none file:mr-4 file:py-1.5 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-black file:bg-zinc-100 file:text-zinc-950 hover:file:bg-white file:transition file:cursor-pointer',
            }),
        }

    # In Python, the __init__ constructor runs automatically when the form class is created.
    # We override it to dynamically inject the active 'user' credentials and filter album choices.
    def __init__(self, *args, **kwargs):
        # We extract the custom 'user' argument from standard keywords parameters dictionary.
        user = kwargs.pop('user', None)
        # We call our parent forms.ModelForm constructor so Django builds standard input schemas.
        super(PhotoForm, self).__init__(*args, **kwargs)
        
        # If the active user has been passed, we filter the album query results.
        # This prevents user A from accidentally uploading or choosing user B's albums!
        if user is not None:
            # We filter the database records so the choices dropdown only displays the user's albums.
            self.fields['album'].queryset = Album.objects.filter(user=user)
            
        # We customize the starting default label in the select dropdown list.
        self.fields['album'].empty_label = "Choose an Album Collection..."
        # We enforce that the user must select an album option to successfully submit the form.
        self.fields['album'].required = True

