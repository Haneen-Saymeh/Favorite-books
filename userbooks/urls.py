from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.regpage),
    path('reg', views.regprocess),
    path('books', views.welcome),
    path('addbook', views.addbook),
    path('login', views.log),
    path('books/<int:id>', views.showbook),
    path('delbook/<int:id>', views.delbook),
    path('editbook/<int:id>', views.updatebook),
    path('addtofav/<int:id>', views.addtofav),
    path('unfav/<int:id>', views.unfav),
    path('logout', views.logout),
   

]