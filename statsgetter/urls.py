from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('export_excel/', views.export_excel, name="export-excel"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('price/', views.price, name="price"),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.success),
    path('cancelled/', views.cancelled),

]
