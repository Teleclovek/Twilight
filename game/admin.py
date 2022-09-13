from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportExportMixin
from .models import Game,Player,Race, RaceDefault, Mapposition

class RaceAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


admin.site.register(Game)
admin.site.register(RaceDefault, RaceAdmin)
admin.site.register(Player)
admin.site.register(Race)
admin.site.register(Mapposition)
