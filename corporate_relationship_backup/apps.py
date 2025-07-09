from django.apps import AppConfig


class CorporateRelationshipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'corporate_relationship'
    verbose_name = 'Corporate Relationship Management'

    def ready(self):
        import corporate_relationship.signals  # noqa
