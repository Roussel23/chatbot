from django.contrib import admin
from .models import Chat
from import_export.admin import ImportExportModelAdmin
# import import_export

# from import_export.admin import ImportExportModelAdmin


# Register your models here.
class ChatAdmin(ImportExportModelAdmin):#admin.ModelAdmin):
    list_display_chat = ('id', 'username','question','response', 'date')
    

admin.site.register(Chat,ChatAdmin)



