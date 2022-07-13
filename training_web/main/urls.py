from django.urls import path, include

from main import views

urlpatterns = [
    path('login/', views.signIn, name='sign_in'),
    path('register/', views.signUp, name='sign_up'),
    path('', views.home, name='home_page'),
    path('postsignUp/', views.postsignUp),
    path('postsignIn/', views.postsignIn),
    path('denoiseImage/', views.denoiseHome, name="denoise_home"),
    path('denoiseImage/<str:username>/', views.denoiseImage, name="denoise"),
    path('imageText/', views.toTextHome, name="imagetext_home"),
    path('imageText/<str:username>/', views.imageToText, name="imagetext"),
    path('profile/', views.profileInfo, name="profile"),
    path('profile/edit/', views.editProfile, name="profile_edit"),
]
