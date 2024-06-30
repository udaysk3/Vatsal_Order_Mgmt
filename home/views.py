from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from user.models import User
from .models import Item, Topup, ChatNote

from django.contrib import messages
from django.db.models import Sum, Count, Q, FloatField
from django.db.models import F, Func, Value, Q, Case, When
from django.db.models.functions import Cast
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def home(request):
    return render(request, "home/index.html")


@login_required
def orders(request):
    if request.user.user_type == "manufacturer":
        orders = Item.objects.filter(assigned_to=request.user, completed=False).order_by('id')
    elif request.user.user_type == "shop":
        orders = Item.objects.filter(shop=request.user).order_by('id')
    else:
        orders = Item.objects.filter(completed=False).order_by('id')

    p_customers = Paginator(orders, 10)
    page_number = request.GET.get("page")
    try:
        page_obj = p_customers.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p_customers.page(1)
    except EmptyPage:
        page_obj = p_customers.page(p_customers.num_pages)

    shops = User.objects.filter(user_type="shop")
    mans = User.objects.filter(user_type="manufacturer")
    return render(
        request, "home/orders.html", {"items": page_obj, "shops": shops, "mans": mans}
    )


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
                'stone_status': request.POST.get('stone_status'),
                'order_id': request.POST.get('order_id'),
                'order_id_2': request.POST.get('order_id_2'),
                'status': request.POST.get('status'),
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
                'customer_email': request.POST.get('customer_email'),
                'customer_mobile': request.POST.get('customer_mobile'),
                'tracking_id': request.POST.get('tracking_id'),
                'shipping_method': request.POST.get('shipping_method'),
                'country': request.POST.get('country'),
                'address': request.POST.get('address'),
            }
            try:
                shop_id = request.POST.get('shop_id')
                shop = User.objects.get(pk=shop_id, user_type="shop")
                order_data['shop'] = shop
            except Exception as e:
                messages.error(request, f"An error occurred while getting the shop {e}")
                return render(request, "home/new_order.html")
            if request.POST.get('completed') == 'on':
                order_data['completed'] = True
            else:
                order_data['completed'] = False
            #print(request.POST)
            if(request.POST["order_date"]):
                order_data["order_date"] = request.POST["order_date"]
                
            if(request.POST["last_date"]):
                order_data["last_date"] = request.POST["last_date"]
                #print("sdfdf")
            if(request.POST["original_delivery_date"]):
                order_data["original_delivery_date"] = request.POST["original_delivery_date"]
            
            Item.objects.create(**order_data)
            messages.success(request, "Order created successfully")
            return redirect('/orders')
        except Exception as e:
            messages.error(request, f"An error occurred while creating the order {e}")
            return render(request, "home/new_order.html")
    shops = User.objects.filter(user_type="shop")
    return render(request, "home/new_order.html", {"shops": shops})

@login_required
def editOrder(request, id):
    order = Item.objects.get(pk=id)
    shops = User.objects.filter(user_type="shop")
    if request.method == 'POST':
        try:
            order.order_id = request.POST.get('order_id', order.getOrderID())
            order.order_id_2 = request.POST.get('order_id_2', order.get2OrderID())
            order.status = request.POST.get('status', order.getStatus())
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
            order.stone_status = request.POST.get('stone_status') if request.POST.get('stone_status') not in ["None", None] else order.stone_status
            order.main_stone1 = request.POST.get('main_stone1') if request.POST.get('main_stone1') not in ["None", None] else order.main_stone1
            order.main_stone2 = request.POST.get('main_stone2') if request.POST.get('main_stone2') not in ["None", None] else order.main_stone2
            order.main_stone3 = request.POST.get('main_stone3') if request.POST.get('main_stone3') not in ["None", None] else order.main_stone3
            order.main_stone4 = request.POST.get('main_stone4') if request.POST.get('main_stone3') not in ["None", None] else order.main_stone4
            order.side_stone1 = request.POST.get('side_stone1') if request.POST.get('side_stone1') not in ["None", None] else order.side_stone1
            order.side_stone2 = request.POST.get('side_stone2') if request.POST.get('side_stone1') not in ["None", None] else order.side_stone2
            order.side_stone3 = request.POST.get('side_stone3') if request.POST.get('side_stone1') not in ["None", None] else order.side_stone3
            order.side_stone4 = request.POST.get('side_stone4') if request.POST.get('side_stone1') not in ["None", None] else order.side_stone4
            order.material_used1 = request.POST.get('material_used1') if request.POST.get('material_used1') not in ["None", None] else order.material_used1
            order.material_used2 = request.POST.get('material_used2') if request.POST.get('material_used1') not in ["None", None] else order.material_used2
            order.material_used3 = request.POST.get('material_used3') if request.POST.get('material_used1') not in ["None", None] else order.material_used3
            order.material_used4 = request.POST.get('material_used4') if request.POST.get('material_used1') not in ["None", None] else order.material_used4
            order.labour1 = request.POST.get('labour1') if request.POST.get('labour1') not in ["None", None] else order.labour1
            order.labour2 = request.POST.get('labour2') if request.POST.get('labour1') not in ["None", None] else order.labour2
            order.labour3 = request.POST.get('labour3') if request.POST.get('labour1') not in ["None", None] else order.labour3
            order.delivery_cost = request.POST.get('delivery_cost', order.getDeliveryCost())
            order.packaging_cost = request.POST.get('packaging_cost', order.getPackagingCost())
            order.total_cost = float(order.getMainStone4()) + float(order.getSideStone4()) + float(order.getMaterialUsed4()) + float(order.getLabour3()) + float(order.getPackagingCost()) + float(order.getDeliveryCost())
            if request.POST.get('original_delivery_date'):
                order.original_delivery_date = request.POST.get('original_delivery_date', order.getOriginalDeliveryDate())
            order.customer_name = request.POST.get('customer_name', order.getCustomerName())
            order.customer_email = request.POST.get('customer_email', order.getCustomerEmail())
            order.customer_mobile = request.POST.get('customer_mobile', order.getCustomerMobile())
            order.tracking_id = request.POST.get('tracking_id', order.getTrackingID())
            order.shipping_method = request.POST.get('shipping_method', order.getShippingMethod())
            order.address = request.POST.get('address', order.getAddress())
            order.country = request.POST.get('country', order.getCountry())
            if request.POST.get('shop_id'):
                order.shop = User.objects.get(pk=request.POST.get('shop_id'))
            
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
    return render(request, 'home/new_order.html', {'item': order, "shops": shops})  # Render the same page with the form data

def filterByShop(request):
    shop_id = request.POST['shop_id']
    if request.user.user_type == "manufacturer":
        orders = Item.objects.filter(assigned_to=request.user, shop=shop_id).order_by('id')
    else:
        orders = Item.objects.filter(shop=shop_id).order_by('id')
    mans = User.objects.filter(user_type="manufacturer")
    shops = User.objects.filter(user_type="shop")
    return render(request, "home/orders.html", {"items": orders, "shops": shops, "mans": mans})

def assign_to_manufacturer(request):
    if request.user.user_type == "manufacturer":
        orders = Item.objects.filter(completed=False, assigned_to=request.user).order_by('id')
    else:
        orders = Item.objects.filter(completed=False).order_by('id')
    shops = User.objects.filter(user_type="shop")
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
        orders = Item.objects.filter(completed=True, assigned_to=request.user).order_by('id')
    else:
        orders = Item.objects.filter(completed=True).order_by('id')
    p_customers = Paginator(orders, 10)
    page_number = request.GET.get("page")
    try:
        page_obj = p_customers.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p_customers.page(1)
    except EmptyPage:
        page_obj = p_customers.page(p_customers.num_pages)
    shops = User.objects.filter(user_type="shop")
    mans = User.objects.filter(user_type="manufacturer")
    return render(
        request, "home/orders.html", {"items": page_obj, "shops": shops, "mans": mans}
    )

def markAsComplete(request,id):
    try:
        # print(id)
        order = Item.objects.get(id=id)
        if order.completed:
            order.completed = False
        else:
            order.completed = True
        order.save()
        messages.success(request, "Order marked as completed")
    except Exception as e:
        messages.error(request, f"An error occurred while marking the order as completed {e}")
    return redirect('/orders')

@login_required
def dashboard(request):
    if request.method == 'GET':
        total_orders = len(Item.objects.filter())
        completed_orders = len(Item.objects.filter(completed=True))
        new_orders = total_orders - completed_orders
        shops = User.objects.filter(user_type="shop")
        total_revenue = 0.0
        shop_details = []
        revenue = 0.0
        for shop in shops:
            #print(shop)
            # Calculate total orders of the shop
            total_shop_orders = Item.objects.filter(shop=shop.id).count()
            
            # Calculate completed orders of the shop
            completed_orders = Item.objects.filter(shop=shop.id, completed=True).count()
            
            # Calculate new orders of the shop (not completed)
            new_orders = total_shop_orders - completed_orders
            
            # Calculate total cost of the shop (sum of total cost of all orders)
            total_cost = Item.objects.filter(shop=shop.id).aggregate(total_cost=Sum('total_cost'))['total_cost']
            obj =  Item.objects.filter(shop=shop.id).first()
            if obj:
                revenue = obj.revenue
            else:
                revenue = 0.0

            shop_details.append({
                'shop': shop,
                'total_orders': total_shop_orders,
                'completed_orders': completed_orders,
                'new_orders': new_orders,
                'total_cost': total_cost if total_cost else 0,  # Handle None value if no orders
                "revenue" : revenue
            })
            total_revenue += revenue
            #print(shop_details)
        return render(request, 'home/dashboard.html', {'shop_details': shop_details, 'total_orders' : total_orders, "new_orders" : new_orders, "completed_orders" : completed_orders, "revenue": revenue, "total_revenue": total_revenue})
    else:
            shop_id = request.POST["shop_id"]
            revenue = request.POST["revenue"]
            item = Item.objects.filter(shop=shop_id).update(revenue=revenue)
            item.save()
            return redirect("/dashboard")  

def editshop(request, shop_id):
    if request.method == "POST":
        try:
            revenue = request.POST["revenue"]
            items = Item.objects.filter(shop = shop_id).update(revenue = revenue)    
            messages.success(request, "Revenue Updated Successfully")
        except Exception as e:
            messages.error(request, "Error while Updating the revenue"+str(e))
        return redirect("/dashboard")
    item = Item.objects.filter(shop = shop_id).first()
    if item:
        revenue = item.revenue
    else:
        revenue = 0.0
    shop = User.objects.filter(id = shop_id).first()
    return render(request, "home/editshop.html", {"revenue" : revenue , "shop" : shop})

def deleteOrder(request, id):
    try:
        order = Item.objects.get(id=id)
        order.delete()
        messages.success(request, "Order deleted successfully")
    except Exception as e:
        messages.error(request, f"An error occurred while deleting the order {e}")
    return redirect('/orders')


@login_required
def editTable(request, id):
    order = Item.objects.get(pk=id)
    if request.method == 'POST':
        try:
            order.stone_status = request.POST.get('stone_status') if request.POST.get('stone_status') not in ["None", None] else order.stone_status 
            order.main_stone1 = request.POST.get('main_stone1') if request.POST.get('main_stone1') not in ["None", None] else order.main_stone1 
            order.main_stone2 = request.POST.get('main_stone2')  if request.POST.get('main_stone2') not in ["None", None] else order.main_stone2 
            order.main_stone3 = request.POST.get('main_stone3') if request.POST.get('main_stone3') not in ["None", None] else order.main_stone3 
            order.main_stone4 = request.POST.get('main_stone4')  if request.POST.get('main_stone4') not in ["None", None] else order.main_stone4
            order.side_stone1 = request.POST.get('side_stone1')  if request.POST.get('side_stone1') not in ["None", None] else order.side_stone1 
            order.side_stone2 = request.POST.get('side_stone2')  if request.POST.get('side_stone2') not in ["None", None] else order.side_stone2 
            order.side_stone3 = request.POST.get('side_stone3')  if request.POST.get('side_stone3') not in ["None", None] else order.side_stone3 
            order.side_stone4 = request.POST.get('side_stone4')   if request.POST.get('side_stone4') not in ["None", None] else order.side_stone4
            order.material_used1 = request.POST.get('material_used1')   if request.POST.get('material_used1') not in ["None", None] else order.material_used1 
            order.material_used2 = request.POST.get('material_used2')  if request.POST.get('material_used2') not in ["None", None] else order.material_used2 
            order.material_used3 = request.POST.get('material_used3')  if request.POST.get('material_used3') not in ["None", None] else order.material_used3 
            order.material_used4 = request.POST.get('material_used4') if request.POST.get('material_used4') not in ["None", None] else order.material_used4
            order.labour1 = request.POST.get('labour1')  if request.POST.get('labour1') not in ["None", None] else order.labour1 
            order.labour2 = request.POST.get('labour2')  if request.POST.get('labour2') not in ["None", None] else order.labour2 
            order.labour3 = request.POST.get('labour3')  if request.POST.get('labour3') not in ["None", None] else order.labour3
            order.delivery_cost = request.POST.get('delivery_cost') if request.POST.get('delivery_cost') not in ["None", None] else order.delivery_cost
            order.packaging_cost = request.POST.get('packaging_cost') if request.POST.get('packaging_cost') not in ["None", None] else order.packaging_cost
            order.optional1 = request.POST.get('optional1') if request.POST.get('optional1') not in ["None", None] else order.optional1 
            order.optional2 = request.POST.get('optional2') if request.POST.get('optional2') not in ["None", None] else order.optional2 
            order.optional3 = request.POST.get('optional3') if request.POST.get('optional3') not in ["None", None] else order.optional3 
            order.optional4 = request.POST.get('optional4') if request.POST.get('optional4') not in ["None", None] else order.optional4 
            order.optional5 = request.POST.get('optional5') if request.POST.get('optional5') not in ["None", None] else order.optional5 
            order.optional6 = request.POST.get('optional6') if request.POST.get('optional6') not in ["None", None] else order.optional6 
            order.optional7 = request.POST.get('optional7') if request.POST.get('optional7') not in ["None", None] else order.optional7 
            order.optional8 = request.POST.get('optional8') if request.POST.get('optional8') not in ["None", None] else order.optional8 
            order.optional11 = request.POST.get('optional11') if request.POST.get('optional11') not in ["None", None] else order.optional11 
            order.optional9 = request.POST.get('optional9') if request.POST.get('optional9') not in ["None", None] else order.optional9 
            order.optional10 = request.POST.get('optional10') if request.POST.get('optional10') not in ["None", None] else order.optional10 
            order.mainsidesum = float(order.getMainStone4()) + float(order.getSideStone4())
            order.materiallaboursum = float(order.getMaterialUsed4()) + float(order.getLabour3())
            order.deliverypackagesum = float(order.getDeliveryCost()) + float(order.getPackagingCost())
            order.total_cost = float(order.getMainStone4()) + float(order.getSideStone4()) + float(order.getMaterialUsed4()) + float(order.getLabour3()) + float(order.getPackagingCost()) + float(order.getDeliveryCost())
            order.save()
            messages.success(request, "Order updated successfully")
            return redirect('/orders')  # Redirect to home page or any other appropriate URL
        except Exception as e:
            messages.error(request, f"An error occurred while updating the order{e}")
            return redirect('/orders')
    return render(request, 'home/new_order.html', {'item': order})


class CastToFloat(Func):
    function = 'CAST'
    template = '%(expressions)s AS FLOAT'

def Gold(request):
    if request.method == "POST":
        try:
            manufacturer = request.POST.get("manufacturer")
            gold = request.POST.get("gold")
            Topup.objects.create(manufacturer=User.objects.get(pk=manufacturer), gold=gold)
            messages.success(request, "Topup done successfully")
            return redirect("/gold")
        except Exception as e:
            messages.error(request, f"An error occurred while adding gold {e}")
            return redirect("/gold")
    manufacturers  = User.objects.filter(user_type="manufacturer")
    try:
        topup_details = []
        man_gold_details = []
        for i in manufacturers:
            topup = Topup.objects.filter(manufacturer=i)
            man_given_gold = 0
            if topup:
                man_given_gold = topup.aggregate(Sum('gold')).get('gold__sum', 0.0)
            qs = Item.objects.filter(assigned_to= i)
            man_used_gold = 0
            if qs:
                man_used_gold = (
                            Item.objects
                            .filter(
                                Q(assigned_to=i) & 
                                (Q(material_used1__iexact="Gold") | Q(material_used1__iexact="gold"))
                            )
                            .annotate(
                                material_used2_float=Case(
                                    When(material_used2__regex=r'^[0-9]+(\.[0-9]+)?$', then=Cast('material_used2', FloatField())),
                                    default=0.0,
                                    output_field=FloatField(),
                                )
                            )
                            .aggregate(material_used2_sum=Sum('material_used2_float'))
                            .get('material_used2_sum', 0.0)
                        )
            if man_used_gold == None:
                man_used_gold = 0.0
            if man_given_gold == None:
                man_given_gold = 0.0
            man_remaining_gold = man_given_gold - man_used_gold
            topup_details.append({
                'manufacturer':i,
                'topup':topup,
                })
            man_gold_details.append({
                'manufacturer':i,
                'man_given_gold': man_given_gold,
                'man_used_gold': man_used_gold,
                'man_remaining_gold': man_remaining_gold
            })
        total_remaining = 0
        for i in man_gold_details:
            total_remaining+= i['man_remaining_gold']
        return render(request, "home/gold.html", {"topup_details": topup_details, "man_gold_details": man_gold_details, "total_remaining": total_remaining, "manufacturers": manufacturers})
    except Exception as e:
        total_remaining = 0
        messages.error(request, f"An error occurred while getting the gold details {e}")
        return render(request, "home/gold.html",{ "topup_details":[], "man_gold_details":[], "total_remaining": total_remaining, "manufacturers": manufacturers})


@login_required
def add_chat_note(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        user  = request.user
        ChatNote.objects.create(item=item, user=user, note=request.POST['note'])
        messages.success(request, "Note Added Successfully")
        return redirect('/orders')
