# Custom ignore list so that it stops ignoring .scss files
from django.contrib.staticfiles.apps import StaticFilesConfig

class CustomStaticFilesConfig(StaticFilesConfig): 
    ignore_patterns = ['*~', '#*#']
