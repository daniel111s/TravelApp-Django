from django.contrib import admin
from .models import Travel, Task

admin.site.register(Task)

@admin.register(Travel)
class TravelAdmin(admin.ModelAdmin):
    # kolumny, ktore bedą wyświetlane na podsumowaniu w panelu admina
    list_display = ('city', 'start_date', 'end_date', 'days_to_go', 'type_of_transport')

    list_filter = ('city', 'type_of_transport',)
    search_fields = ('city','type_of_transport','description',)