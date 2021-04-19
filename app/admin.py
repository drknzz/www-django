from django.contrib import admin
from .models import User, Directory, File, SectionCategory, Status, StatusData, FileSection

# Register your models here.
admin.site.register(User)
admin.site.register(Directory)
admin.site.register(File)
admin.site.register(SectionCategory)
admin.site.register(Status)
admin.site.register(StatusData)
admin.site.register(FileSection)