from django.urls import path
from . import views

app_name = 'crypto'

urlpatterns = [
    path('', views.home, name="home"),
    path('prices/', views.prices, name="prices"),
    path('portfolio/', views.portfolio, name="portfolio"),
    path('portfolio/profile', views.portfolioProfile, name="profile"),
    path('portfolio/create', views.portfolioCreate, name="create"),
    path('portfolio/edit_<int:portfolio_id>', views.portfolioEdit, name="edit")
]
