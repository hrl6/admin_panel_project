from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        from django.contrib import admin
        from django.contrib.admin import AdminSite

        admin.site.site_header = 'Company Management System'
        admin.site.site_title = 'Admin Panel'
        admin.site.index_title = 'Welcome to Management Portal'