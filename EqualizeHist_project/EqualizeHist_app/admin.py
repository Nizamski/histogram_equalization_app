from django.contrib import admin

# Register your models here.
from EqualizeHist_app.models import Image, Histogram, EqualizedHistogram, EqualizedImage


class ImageAdmin(admin.ModelAdmin):
    class Meta:
        model = Image

class HistogramAdmin(admin.ModelAdmin):
    class Meta:
        model = Histogram

class EqualizedImageAdmin(admin.ModelAdmin):
    class Meta:
        model = EqualizedImage

class EqualizedHistogramAdmin(admin.ModelAdmin):
    class Meta:
        model = EqualizedHistogram


admin.site.register(Image, ImageAdmin)
admin.site.register(Histogram, HistogramAdmin)
admin.site.register(EqualizedImage, EqualizedImageAdmin)
admin.site.register(EqualizedHistogram, EqualizedHistogramAdmin)
