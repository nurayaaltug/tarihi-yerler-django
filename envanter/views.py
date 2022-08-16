from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q

def index(request):
    tarihi_yer_sayisi = TarihiYer.objects.all().count()
    iller = Il.objects.all()
    yerlesim_sekilleri = YerlesimTuru.objects.all()

   
    #print(resimler)

    son_5_yer = TarihiYer.objects.filter().order_by('-id')[:8]
    count = 0
    for yer in son_5_yer:
        yerResimleri = Resim.objects.filter(tarihi_yer=yer)
        if(len(yerResimleri) > 0):
           son_5_yer[count].resimAdi = yerResimleri[0].resim
        count += 1

    context = {
        "tarihi_yer_sayisi" : tarihi_yer_sayisi,
        "yerlesim_sekilleri" : yerlesim_sekilleri,
        "iller" : iller,
        "title" : "Ana Sayfa",
        "son_5_yer" : son_5_yer,
    }
    return render(request,"index.html", context)

def giris(request):
    tarihi_yer_sayisi = TarihiYer.objects.all().count()
    iller = Il.objects.all()
    yerlesim_sekilleri = YerlesimTuru.objects.all()
    context = {
        "tarihi_yer_sayisi": tarihi_yer_sayisi,
        "yerlesim_sekilleri": yerlesim_sekilleri,
        "iller": iller,
        "title": "Giriş Yap"
    }
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "" or password == "":
            messages.error(request,"Tüm alanlar zorunludur.")
        else:
            user = authenticate(username = username, password = password)
            if user:
                login(request,user)
                messages.success(request,"Başarılı bir şekilde giriş yapıldı.")
                return redirect('index')
            else:
                messages.error(request,"Böyle bir kullanıcı bulunamadı.")

    return render(request,"giris.html",context)

def kayit(request):
    tarihi_yer_sayisi = TarihiYer.objects.all().count()
    iller = Il.objects.all()
    yerlesim_sekilleri = YerlesimTuru.objects.all()
    context = {
        "tarihi_yer_sayisi": tarihi_yer_sayisi,
        "yerlesim_sekilleri": yerlesim_sekilleri,
        "iller": iller,
        "title": "Kayıt Ol"
    }
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username == "" or email == "" or password == "":
            messages.error(request,"Tüm alanlar zorunludur.")
        else:
            if User.objects.filter(username = username).exists():
                messages.error(request,"Bu kullanıcı adına sahip bir kullanıcı zaten var.")
            elif User.objects.filter(email = email).exists():
                messages.error(request, "Bu e-posta adresine sahip bir kullanıcı zaten var.")
            else:
                user = User()
                user.username = username
                user.email = email
                user.set_password(password)
                user.save()
                messages.success(request,"Başarıyla kayıt olundu ve giriş yapıldı.")
                login(request,user)
                return redirect("index")
    return render(request,"kayit.html",context)


def ile_gore_listele(request,id):
    il = Il.objects.get(id = id)
    yerler = TarihiYer.objects.filter(il = il)
    iller = Il.objects.all()
    yerlesim_sekilleri = YerlesimTuru.objects.all()
    context = {
        "il" : il,
        "yerler" : yerler,
        "title" : "{} ilindeki tarihi yerler".format(il.adi),
        "yerlesim_sekilleri": yerlesim_sekilleri,
        "iller": iller,
    }
    return render(request,"ilegore.html",context)


def ture_gore_listele(request,id):
    tur = YerlesimTuru.objects.get(id = id)
    yerler = TarihiYer.objects.filter(yerlesim_turu = tur)
    iller = Il.objects.all()
    yerlesim_sekilleri = YerlesimTuru.objects.all()
    context = {
        "tur" : tur,
        "yerler" : yerler,
        "title" : "{} türündeki tarihi yerler".format(tur.adi),
        "yerlesim_sekilleri": yerlesim_sekilleri,
        "iller": iller,
    }
    return render(request,"turegore.html",context)

@login_required
def cikis(request):
    logout(request)
    messages.success(request,"Başarıyla çıkış yapıldı.")
    return redirect('index')
@login_required
def ekle(request):
    iller = Il.objects.all()
    yerlesim_sekilleri = YerlesimTuru.objects.all()
    context = {
        "yerlesim_sekilleri": yerlesim_sekilleri,
        "iller": iller,
        "title": "Ekle",
    }

    if request.method == "POST":
        name = request.POST.get("name")
        city = request.POST.get("city")
        district = request.POST.get("district")
        type_ = request.POST.get("type")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        details = request.POST.get("details")
        files = request.FILES.getlist("files")

        if name == "" or city == "" or district == "" or type == "" or latitude == "" or longitude == "" or details == "":
            messages.error(request,"Tüm alanlar zorunludur.")
        elif TarihiYer.objects.filter(isim = name).exists():
            messages.error(request,"Bu isimli bir tarihi alan zaten eklenmiş.")
        else:
            city_obj = Il.objects.get(id = city)
            type_obj = YerlesimTuru.objects.get(id = type_)
            new = TarihiYer()
            new.isim = name
            new.ekleyen = request.user
            new.aciklama = details
            new.enlem = latitude
            new.boylam = longitude
            new.ilce = district
            new.il = city_obj
            new.yerlesim_turu = type_obj
            new.save()
            for i in files:
                resim = Resim()
                resim.resim = i
                resim.tarihi_yer = new
                resim.save()

            messages.success(request,"Başarılı bir şekilde eklendi.")
            return redirect("detay", new.id)

    return render(request,"ekle.html", context)

def detay(request,id):
    if not TarihiYer.objects.filter(id = id).exists():
        messages.error(request,"Böyle bir tarihi yer bulunamadı.")
        return redirect("index")

    yer = TarihiYer.objects.get(id=id)
    resimler = Resim.objects.filter(tarihi_yer=yer)
    iller = Il.objects.all()
    yerlesim_sekilleri = YerlesimTuru.objects.all()
    context = {
        "yer" : yer,
        "resimler" : resimler,
        "title" : "{}".format(yer.isim),
        "yerlesim_sekilleri": yerlesim_sekilleri,
        "iller": iller,
        "enlem" : float(yer.enlem),
        "boylam" : float(yer.boylam)
    }

    return render(request,"detay.html",context)

def search(request):

    if request.method == "POST":
        q = request.POST.get('search').strip()
        iller = Il.objects.all()
        yerlesim_sekilleri = YerlesimTuru.objects.all()
        yerler = TarihiYer.objects.filter(Q(isim__icontains=q)).order_by('-id')
        context = {
            "yerlesim_sekilleri": yerlesim_sekilleri,
            "iller": iller,
            "title": "{} anahtar kelimesi ile arama".format(q),
            "yerler" : yerler
        }
        return render(request,"search.html",context)
    else:
        return redirect('index')