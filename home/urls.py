from . import views
from django.urls import path

app_name = "app"

urlpatterns = [
    path("", views.home),
    path("dashboard", views.dashboard),
    path("orders", views.orders, name="orders"),
    path("adminview", views.Admin, name="admin"),
    path("new_order", views.newOrder, name="new_order"),
    path("edit_order/<str:id>", views.editOrder, name="edit_order"),
    path("filterbyshop", views.filterByShop, name="filterbyshop"),
    path("completed_orders", views.completedOrders, name="completed_orders"),
    path("markascomplete/<str:id>", views.markAsComplete, name="markascomplete"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("editshop/<str:shop>", views.editshop, name="editshop")
    ]