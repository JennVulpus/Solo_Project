from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard',views.dashboard),
    path('ToCampaignDatabase',views.create_campaign),
    path('create_campaign',views.render_create_campaign),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('delete_campaign/<int:campaign_id>',views.delete_campaign),
    path('delete_character/<int:character_id>',views.delete_character),
    path('ToCharacterDatabase',views.create_character),
    path('create_character', views.render_create_character),
    path('view_campaign/<int:campaign_id>', views.view_campaign),
    path('view_character/<int:character_id>', views.view_character),
    path('edit_campaign/<int:campaign_id>',views.edit_campaign),
    path('edit_character/<int:character_id>',views.edit_character),
    path('save_campaign/<int:campaign_id>',views.save_campaign),
    path('save_character/<int:character_id>',views.save_character),
]