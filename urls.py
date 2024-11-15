# myapp/urls.py

from django.urls import path
from . import views
from .views import Usercbv, LabGroupView

app_name = 'myapp'  # Namespace for app URLs

urlpatterns = [

    path('', views.index, name='index'),  # Root URL for the app
   path('about/', views.about, name='about'),  # Optional about page without parameters
    path('about/<int:year>/<int:month>/', views.about, name='about'),  # With year and month parameters
    path('type/<int:type_no>/', views.detail, name='detail'),  # URL for detail view with type_no parameter
    # path('user/', views.user_FBV, name='user_FBV'),  # Uncomment if using function-based view
    path('user/', Usercbv.as_view(), name='user_list'),  # URL for class-based view
path('lab-group/', LabGroupView.as_view(), name='lab_group'),
path('items/', views.items, name='items'),
    path('placeorder/', views.place_order, name='placeorder'),
path('signup/', views.SignUpView.as_view(), name='signup'),
path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
path('myorders/', views.myorders, name='myorders'),
    path('interest/<int:item_id>/', views.show_interest, name='show_interest'),  # Updated to accept item_id

]
