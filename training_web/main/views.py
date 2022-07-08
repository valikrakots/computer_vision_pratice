import os

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from main.static.main.scripts import denoise


# def validate_file_extension(value):
#   import os
#   ext = os.path.splitext(value.name)[1]
#   valid_extensions = ['.pdf','.doc','.docx']
#   if not ext in valid_extensions:
#     raise ValidationError(u'File not supported!')


def home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, "main/home.html")
    else:
        return signIn(request)


def signIn(request):
    return render(request, "main/login.html")



def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        user = authenticate(username=email, password=pasw)
        if user is None:
            raise Exception("")
        request.user = user
    except:
        message = "Invalid Credentials!!"
        return render(request, "main/login.html", {"message": message})

    return home(request)


def signUp(request):
    return render(request,"main/register.html")


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

    except Exception as e:
        print(e)
        msg = str(e)
        content = {
            'message': msg,
        }
        return render(request, "main/register.html", content)
    return render(request, "main/login.html")


def denoiseImage(request, username):
    uploadedFile = request.FILES.get('image_to_process')
    fs = FileSystemStorage()
    username =  username.replace('@', '')
    filename = fs.save('images/' + username + '.' + uploadedFile.name, uploadedFile)
    uploaded_file_url = fs.url(filename)
    print(uploaded_file_url)
    img = denoise.predict(uploaded_file_url)
    os.remove(uploaded_file_url[1:])
    img = img.convert('L')
    response = HttpResponse(content_type='image/png')
    img.save(response, "png")
    response['Content-Disposition'] = 'attachment; filename="denoised_image.png"'
    # response = HttpResponse(img, content_type='application/force-download')
    # response['Content-Disposition'] = 'attachment; filename=' + 'denoised_image.png'
    return response
