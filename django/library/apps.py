"""
Library application configuration for Django

Defines application-specific settings, including:
- Path to templates
- Signal configuration
- Application metadata
"""
from django.apps import AppConfig

class LibraryConfig(AppConfig):
    """
    Configuration class for the main library application

    Attributes:
        default_auto_field (str): Type of default auto field
        name (str): Name of the application according to Django convention
    Methods:
        ready(): Initializes signals and other startup components
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'

    def ready(self):
        """
        Initializes signals and other startup components
        """ 
        import library.signals 