from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user.models import User
from .models import Item
from django.contrib import messages
from django.db.models import Sum, Count
# Create your views here.


def home(request):
    return render(request, "home/index.html")


@login_required
def dashboard(request):
    return render(request, "home/dashboard.html")


@login_required
def orders(request):
    if request.user.user_type == "manufacturer":
        orders = Item.objects.filter(assigned_to=request.user, completed=False)
    else:
        orders = Item.objects.filter(completed=False)
    shops = Item.objects.values('shop_name').distinct()
    mans = User.objects.filter(user_type="manufacturer")
    return render(request, "home/orders.html", {"items": orders, "shops" : shops, "mans": mans})


@login_required
def Admin(request):
    if request.GET.get("page") == "edit":
        user_id = request.GET.get("id")
        user = User.objects.get(pk=user_id)
        return render(request, "home/admin.html", {"user": user})
    users = User.objects.filter(is_superuser=False).values
    return render(request, "home/admin.html", {"users": users})

@login_required
def newOrder(request):
    if request.method == "POST":
        try:
            order_data = {
                'order_id': request.POST.get('order_id'),
                'order_id_2': request.POST.get('order_id_2'),
                'order_date': request.POST.get('order_date'),
                'admin_photo': request.FILES.get('admin_photo'),
                'manufacturer_photo': request.FILES.get('manufacturer_photo'),
                'title': request.POST.get('title'),
                'quantity': request.POST.get('quantity'),
                'material': request.POST.get('material'),
                'color': request.POST.get('color'),
                'size': request.POST.get('size'),
                'personalization': request.POST.get('personalization'),
                'main_stone1': request.POST.get('main_stone1'),
                'main_stone2': request.POST.get('main_stone2'),
                'main_stone3': request.POST.get('main_stone3'),
                'main_stone4': request.POST.get('main_stone4', 0.0),
                'side_stone1': request.POST.get('side_stone1'),
                'side_stone2': request.POST.get('side_stone2'),
                'side_stone3': request.POST.get('side_stone3'),
                'side_stone4': request.POST.get('side_stone4', 0.0),
                'material_used1': request.POST.get('material_used1'),
                'material_used2': request.POST.get('material_used2'),
                'material_used3': request.POST.get('material_used3'),
                'material_used4': request.POST.get('material_used4', 0.0),
                'labour1': request.POST.get('labour1'),
                'labour2': request.POST.get('labour2'),
                'labour3': request.POST.get('labour3', 0.0),
                'delivery_cost': request.POST.get('delivery_cost', 0),
                'packaging_cost': request.POST.get('packaging_cost', 0),
                'total_cost': request.POST.get('total_cost', 0),
                'customer_name': request.POST.get('customer_name'),
                'fast_shipping': request.POST.get('fast_shipping', False),
                'address': request.POST.get('address'),
                'shop_name': request.POST.get('shop_name'),
                'completed': request.POST.get('completed', False),
            }
            print(request.POST)
            if(request.POST["order_date"]):
                order_data["order_date"] = request.POST["order_date"]
                
            if(request.POST["last_date"]):
                order_data["last_date"] = request.POST["last_date"]
                print("sdfdf")
            if(request.POST["original_delivery_date"]):
                order_data["original_delivery_date"] = request.POST["original_delivery_date"]
            
            Item.objects.create(**order_data)
            messages.success(request, "Order created successfully")
            return redirect('/orders')
        except Exception as e:
            messages.error(request, f"An error occurred while creating the order {e}")
            return render(request, "home/new_order.html")
    return render(request, "home/new_order.html")

@login_required
def editOrder(request, id):
    order = Item.objects.get(pk=id)
    if request.method == 'POST':
        try:
            order.order_id = request.POST.get('order_id', order.getOrderID())
            order.order_id_2 = request.POST.get('order_id_2', order.get2OrderID())
            order.order_date = request.POST.get('order_date', order.getOrderDate())
            if request.FILES.get('admin_photo'):
                order.admin_photo = request.FILES.get('admin_photo')
            if request.FILES.get('manufacturer_photo'):
                order.manufacturer_photo = request.FILES.get('manufacturer_photo')
            order.title = request.POST.get('title', order.getTitle())
            order.quantity = request.POST.get('quantity', order.getQuantity())
            order.material = request.POST.get('material', order.getMaterial())
            order.color = request.POST.get('color', order.getColor())
            order.size = request.POST.get('size', order.getSize())
            order.personalization = request.POST.get('personalization', order.getPersonalization())
            if request.POST.get('last_date'):
                order.last_date = request.POST.get('last_date', order.getLastDate())
            order.main_stone1 = request.POST.get('main_stone1', order.getMainStone1())
            order.main_stone2 = request.POST.get('main_stone2', order.getMainStone2())
            order.main_stone3 = request.POST.get('main_stone3', order.getMainStone3())
            order.main_stone4 = request.POST.get('main_stone4', order.getMainStone4())
            order.side_stone1 = request.POST.get('side_stone1', order.getSideStone1())
            order.side_stone2 = request.POST.get('side_stone2', order.getSideStone2())
            order.side_stone3 = request.POST.get('side_stone3', order.getSideStone3())
            order.side_stone4 = request.POST.get('side_stone4', order.getSideStone4())
            order.material_used1 = request.POST.get('material_used1', order.getMaterialUsed1())
            order.material_used2 = request.POST.get('material_used2', order.getMaterialUsed2())
            order.material_used3 = request.POST.get('material_used3', order.getMaterialUsed3())
            order.material_used4 = request.POST.get('material_used4', order.getMaterialUsed4())
            order.labour1 = request.POST.get('labour1', order.getLabour1())
            order.labour2 = request.POST.get('labour2', order.getLabour2())
            order.labour3 = request.POST.get('labour3', order.getLabour3())
            order.delivery_cost = request.POST.get('delivery_cost', order.getDeliveryCost())
            order.packaging_cost = request.POST.get('packaging_cost', order.getPackagingCost())
            order.total_cost = float(order.getMainStone4()) + float(order.getSideStone4()) + float(order.getMaterialUsed4()) + float(order.getLabour3()) + float(order.getPackagingCost()) + float(order.getDeliveryCost())
            if request.POST.get('original_delivery_date'):
                order.original_delivery_date = request.POST.get('original_delivery_date', order.getOriginalDeliveryDate())
            order.customer_name = request.POST.get('customer_name', order.getCustomerName())
            order.address = request.POST.get('address', order.getAddress())
            order.shop_name = request.POST.get('shop_name', order.getShopName())
            if request.POST.get('fast_shipping') == 'on':
                order.fast_shipping = True
            else:
                order.fast_shipping = False
            if request.POST.get('completed') == 'on':
                order.completed = True
            else:
                order.completed = False
            order.save()
            messages.success(request, "Order updated successfully")
            return redirect('/orders')  # Redirect to home page or any other appropriate URL
        except Exception as e:
            messages.error(request, f"An error occurred while updating the order{e}")
            return render(request, 'home/new_order.html', {'item': order})
    return render(request, 'home/new_order.html', {'item': order})

def filterByShop(request):
    shop_name = request.POST['shop_name']
    if request.user.user_type == "manufacturer":
        orders = Item.objects.filter(assigned_to=request.user, shop_name=shop_name)
    else:
        orders = Item.objects.filter(shop_name=shop_name)
    mans = User.objects.filter(user_type="manufacturer")
    shops = Item.objects.values('shop_name').distinct()
    return render(request, "home/orders.html", {"items": orders, "shops": shops, "mans": mans})

def assign_to_manufacturer(request):
    if request.user.user_type == "manufacturer":
        orders = Item.objects.filter(completed=False, assigned_to=request.user)
    else:
        orders = Item.objects.filter(completed=False)
    shops = Item.objects.values('shop_name').distinct()
    mans = User.objects.filter(user_type="manufacturer")
    if request.method == "GET":
        return render(request, "home/orders.html", {"items": orders, "shops": shops, "mans": mans})
    manufacturer = request.POST['manufacturer']
    man = User.objects.get(id=manufacturer)
    item = Item.objects.get(id=request.POST['order'])
    item.assigned_to = man
    item.save()
    messages.success(request, "Order assigned to manufacturer")
    return render(request, "home/orders.html", {"items": orders, "shops": shops, "mans": mans})

def completedOrders(request):
    if request.user.user_type == "manufacturer":
        orders = Item.objects.filter(completed=True, assigned_to=request.user)
    else:
        orders = Item.objects.filter(completed=True)
    shops = Item.objects.values('shop_name').distinct()
    mans = User.objects.filter(user_type="manufacturer")
    return render(request, "home/orders.html", {"items": orders, "shops": shops, "mans": mans})

def markAsComplete(request,id):
    try:
        print(id)
        order = Item.objects.get(id=id)
        order.completed = True
        order.save()
        messages.success(request, "Order marked as completed")
    except Exception as e:
        messages.error(request, f"An error occurred while marking the order as completed {e}")
    return redirect('/orders')

def dashboard(request):
    if request.method == 'GET':
        total_orders = len(Item.objects.filter())
        completed_orders = len(Item.objects.filter(completed=True))
        new_orders = total_orders - completed_orders
        shops = set(Item.objects.values_list('shop_name', flat=True))
        total_revenue = 0.0
        shop_details = []
        revenue = 0.0
        for shop in shops:
            print(shop)
            # Calculate total orders of the shop
            total_shop_orders = Item.objects.filter(shop_name=shop).count()
            
            # Calculate completed orders of the shop
            completed_orders = Item.objects.filter(shop_name=shop, completed=True).count()
            
            # Calculate new orders of the shop (not completed)
            new_orders = total_shop_orders - completed_orders
            
            # Calculate total cost of the shop (sum of total cost of all orders)
            total_cost = Item.objects.filter(shop_name=shop).aggregate(total_cost=Sum('total_cost'))['total_cost']
            revenue =  Item.objects.filter(shop_name=shop).first().revenue

            shop_details.append({
                'shop_name': shop,
                'total_orders': total_shop_orders,
                'completed_orders': completed_orders,
                'new_orders': new_orders,
                'total_cost': total_cost if total_cost else 0,  # Handle None value if no orders
                "revenue" : revenue
            })
            total_revenue += revenue
            print(shop_details)
        return render(request, 'home/dashboard.html', {'shop_details': shop_details, 'total_orders' : total_orders, "new_orders" : new_orders, "completed_orders" : completed_orders, "revenue": revenue, "total_revenue": total_revenue})
    else:
            shop_name = request.POST["shop_name"]
            revenue = request.POST["revenue"]
            item = Item.objects.filter(shop_name=shop_name).update(revenue=revenue)
            item.save()
            return redirect("/dashboard")  
        
def editshop(request, shop):
    if request.method == "POST":
        try:
            revenue = request.POST["revenue"]
            items = Item.objects.filter(shop_name = shop).update(revenue = revenue)    
            messages.success(request, "Revenue Updated Successfully")
        except Exception as e:
            messages.error(request, "Error while Updating the revenue"+str(e))
        return redirect("/dashboard")
    item = Item.objects.filter(shop_name = shop).first()
    return render(request, "home/editshop.html", {"revenue" : item.revenue , "shop" : shop})

def deleteOrder(request, id):
    try:
        order = Item.objects.get(id=id)
        order.delete()
        messages.success(request, "Order deleted successfully")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the order {e}")
    return redirect('/orders')