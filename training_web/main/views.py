import os
import logging
from io import BytesIO

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.static.main.scripts import denoise
from main.static.main.scripts import totext
from .forms import EditProfileForm
from .models import Result, CalculationCount

logger = logging.getLogger('default')


# def validate_file_extension(value):
#   import os
#   ext = os.path.splitext(value.name)[1]
#   valid_extensions = ['.pdf','.doc','.docx']
#   if not ext in valid_extensions:
#     raise ValidationError(u'File not supported!')


def home(request):
    if request.user.is_authenticated:
        return render(request, "main/home.html")
    else:
        logger.info("Unauthenticated user appeared")
        return signIn(request)


def signIn(request):
    return render(request, "main/login.html")


def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        user = authenticate(username=email, email=email, password=pasw)
        if user is None:
            raise Exception("Wrong credentials")
        auth_login(request, user)
        logger.warning("User " + request.user.username + " authenticated")
    except:
        logger.warning("User passed wrong credentials")
        message = "Invalid Credentials!!"
        return render(request, "main/login.html", {"message": message})

    return home(request)


def signUp(request):
    return render(request, "main/register.html")


def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    rep_pass = request.POST.get('pass_repeat')
    try:
        if passs != rep_pass:
            raise Exception("Passwords should match")
        if len(passs) < 6:
            raise Exception("Password should be at least 6 characters long")
        # creating a user with the given email and password
        user = User.objects.create_user(email, email, passs)
        user.save()
        count = CalculationCount(user=user)
        count.save()
        logger.info("New user registered")

    except Exception as e:
        msg = str(e)
        content = {
            'message': msg,
        }
        logger.warning("User failed to register, cause: " + str(e))
        return render(request, "main/register.html", content)
    return render(request, "main/login.html")


def denoiseHome(request):
    return render(request, "main/denoiseImage.html")


def toTextHome(request):
    return render(request, "main/imageText.html")


def denoiseImage(request, username):
    uploadedFile = request.FILES.get('image_to_process')
    fs = FileSystemStorage()
    username = username.replace('@', '')
    filename = fs.save('images/' + username + '.' + uploadedFile.name, uploadedFile)
    uploaded_file_url = fs.url(filename)
    img = denoise.predict(uploaded_file_url)
    os.remove(uploaded_file_url[1:])
    img = img.convert('L')
    response = HttpResponse(content_type='image/png')
    img.save(response, "png")
    response['Content-Disposition'] = 'attachment; filename="denoised_' + uploadedFile.name + '"'

    path = 'media/results/' + username + "." + uploadedFile.name
    img.save(path)
    result = Result(user=request.user)
    result.res_image = path[6:]
    result.save()

    calc_count = CalculationCount.objects.all().get(user=request.user)
    calc_count.count += 1
    calc_count.save()

    # response = HttpResponse(img, content_type='application/force-download')
    # response['Content-Disposition'] = 'attachment; filename=' + 'denoised_image.png'
    return response


def imageToText(request, username):
    uploadedFile = request.FILES.get('image_to_process')
    fs = FileSystemStorage()
    username = username.replace('@', '')
    filename = fs.save('images/' + username + '.' + uploadedFile.name, uploadedFile)
    uploaded_file_url = fs.url(filename)
    text = totext.convert(uploaded_file_url)

    result = Result(user=request.user, res_text=text)
    result.save()

    calc_count = CalculationCount.objects.all().get(user=request.user)
    calc_count.count += 1
    calc_count.save()

    os.remove(uploaded_file_url[1:])
    return render(request, 'main/imageText.html', {"text": text})


def profileInfo(request):
    try:
        count = CalculationCount.objects.all().get(user=request.user)
        return render(request, "main/profile.html", {"user": request.user, "count": count.count})
    except:
        count = CalculationCount(user=request.user)
        count.save()
        return render(request, "main/profile.html", {"user": request.user, "count": count.count})


def editProfile(request):
    if request.method == 'POST':

        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile/')

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'main/editProfile.html', {'form': form})

