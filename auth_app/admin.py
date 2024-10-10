from django.contrib import admin
from .models import CV_Model, UploadedCV

# Register your models here.
class CV_Model_Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_at', 'cv_file', 'cv_text')
    list_filter = ('id', 'user')
    search_fields = ('id', 'user')

class UploadedCv_Model_Admin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_at', 'cv_file')
    list_filter = ('id', 'user')
    search_fields = ('id', 'user')


admin.site.register(CV_Model, CV_Model_Admin)
admin.site.register(UploadedCV, UploadedCv_Model_Admin)