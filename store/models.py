from django.db import models

class Product(models.Model):
    in_stock = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=211)
    image1 = models.ImageField(upload_to='images', null=True, blank=True) #default="picture.png"
    image2 = models.ImageField(upload_to='images', null=True, blank=True)
    image3 = models.ImageField(upload_to='images', null=True, blank=True) 
    video = models.FileField(upload_to='videos', null=True, blank=True)

    def __str__(self):
    	return self.name

    def delete(self, *args, **kwargs):
        self.image1.delete()
        self.image2.delete()
        self.image3.delete()
        self.video.delete()
        super().delete(*args, **kwargs)