from django.urls import path
from . import views

urlpatterns = [
    path('api/convert/', views.convert_po_to_mo, name='convert'),
].
