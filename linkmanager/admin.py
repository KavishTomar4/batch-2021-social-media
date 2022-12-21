from django.contrib import admin
from .models import CustomUser
from .models import PhotoUpload
from .models import Comments
from .models import Notification
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PhotoUpload)
admin.site.register(Comments)
admin.site.register(Notification)
