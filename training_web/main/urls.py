from django.urls import path, include

from main import views

urlpatterns = [
    path('login/', views.signIn, name='sign_in'),
    path('register/', views.signUp, name='sign_up'),
    path('', views.home, name='home_page'),
    path('postsignUp/', views.postsignUp),
    path('postsignIn/', views.postsignIn),
    path('denoiseImage/<str:username>/', views.denoiseImage, name="denoise"),
]
