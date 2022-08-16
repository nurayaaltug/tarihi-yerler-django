from django.db import models


class Il(models.Model):
    adi = models.CharField(max_length=50)

class YerlesimTuru(models.Model):
    adi = models.CharField(max_length=50,verbose_name="Yerleşim türü")

class TarihiYer(models.Model):
    isim = models.CharField(max_length=300,verbose_name="Tarihin yerin adı")
    ekleyen = models.ForeignKey("auth.User",on_delete=models.CASCADE,verbose_name="Ekleyen kullanıcı")
    aciklama = models.TextField(max_length=5000,verbose_name="Detaylar")
    enlem = models.FloatField(verbose_name="Enlem")
    boylam = models.FloatField(verbose_name="Boylam")
    il = models.ForeignKey("Il",on_delete=models.CASCADE)
    ilce = models.CharField(max_length=50,verbose_name="İlçe")
    yerlesim_turu = models.ForeignKey("YerlesimTuru",on_delete=models.CASCADE)

class Resim(models.Model):
    resim = models.ImageField()
    tarihi_yer = models.ForeignKey("TarihiYer",on_delete=models.CASCADE)

