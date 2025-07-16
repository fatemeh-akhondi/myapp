from django.apps import AppConfig


class TestitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testit'
    
    def ready(self):
        import testit.signals
