from . import views
from django.urls import path

app_name = "app"

urlpatterns = [
    path("", views.home),
    path("dashboard", views.dashboard),
    path("orders", views.orders, name="orders"),
    path("adminview", views.Admin, name="admin"),
    path("gold", views.Gold, name="gold"),
    path("new_order", views.newOrder, name="new_order"),
    path("edit_order/<str:id>", views.editOrder, name="edit_order"),
     path("edit_table/<str:id>", views.editTable, name="edit_table"),
    path("delete_order/<str:id>", views.deleteOrder, name="delete_order"),
    path("filterbyshop", views.filterByShop, name="filterbyshop"),
    path("assign_to_manufacturer", views.assign_to_manufacturer, name="assign_to_manufacturer"),
    path("completed_orders", views.completedOrders, name="completed_orders"),
    path("markascomplete/<str:id>", views.markAsComplete, name="markascomplete"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("editshop/<str:shop_id>", views.editshop, name="editshop"),
    path('item/<int:item_id>/add_chat_note/', views.add_chat_note, name='add_chat_note'),
    ]