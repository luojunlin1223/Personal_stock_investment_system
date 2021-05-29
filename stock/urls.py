from django.urls import path

from stock import views
app_name = 'stock'
urlpatterns = [
    path('info/',views.showinfo,name="showinfo"),
    path('detail/',views.showdetail,name="show_detail"),
    path('read/',views.read_data,name="read_data"),
    path('delete/',views.delete_data,name="delete_data"),
    path('search/',views.search,name="search"),

    path('addfavorite/',views.add_favorite,name="add_favorite"),
    path('collections/',views.read_favorite,name="read_favorite"),
    path('delefavorite/',views.delete_favorite,name="delete_favorite"),
    path('alterfavorite/price',views.alter_favorite_price,name="alter_favorite_price"),
    path('alterfavorite/count',views.alter_favorite_count,name="alter_favorite_count"),


    path('createconditions',views.create_condisitons,name="create_conditions"),
    path('addconditions/',views.add_conditions,name="add_conditions"),
    path('conditions/',views.conditions,name="conditions"),
    path('conditions/change',views.change_conditions,name="change_conditions"),
    path('conditions/delete',views.delete_condisitons,name="delete_conditions"),


    path('company/',views.read_company,name="read_company"),
    path('interest/',views.interest,name="interest"),
]