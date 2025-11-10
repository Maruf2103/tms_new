from django.db import models

class TmsCoreSetting(models.Model):
    setting_key = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.setting_key}: {self.setting_value}"

    class Meta:
        verbose_name = "TMS Core Setting"
        verbose_name_plural = "TMS Core Settings"
