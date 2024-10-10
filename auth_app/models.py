from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CV_Model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateField(auto_now_add=True)
    cv_file = models.FileField(upload_to='uploads/cvs/')
    cv_text = models.TextField()

    def __str__(self):
        return f"CV uploaded by {self.user.username}"


class UploadedCV(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cv_file = models.FileField(upload_to='uploads/cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CV uploaded by {self.user.username}"
