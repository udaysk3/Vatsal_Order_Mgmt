from django.db import models
from user.models import User

class Item(models.Model):
    order_id = models.CharField(max_length=100)
    order_id_2 = models.CharField(max_length=100)
    status = models.CharField(max_length=100, blank = True, null= True)
    order_date = models.DateField()
    admin_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank = True, null= True)
    manufacturer_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank = True, null= True)
    title = models.CharField(max_length=100, blank = True, null= True)
    quantity = models.IntegerField(default=1)
    material = models.CharField(max_length=100, blank = True, null= True)
    color = models.CharField(max_length=100, blank = True, null= True)
    size = models.CharField(max_length=100, blank = True, null= True)
    personalization = models.CharField(max_length=100, blank = True, null= True)
    last_date = models.DateField(blank = True, null= True)
    main_stone1 = models.CharField(max_length=100, blank = True, null= True)
    main_stone2 = models.CharField(max_length=100, blank = True, null= True)
    main_stone3 = models.CharField(max_length=100, blank = True, null= True)
    main_stone4 = models.FloatField(default=0)
    side_stone1 = models.CharField(max_length=100, blank = True, null= True)
    side_stone2 = models.CharField(max_length=100, blank = True, null= True)
    side_stone3 = models.CharField(max_length=100, blank = True, null= True)
    side_stone4 = models.FloatField(default=0)
    material_used1 = models.CharField(max_length=100, blank = True, null= True)
    material_used2 = models.CharField(max_length=100, blank = True, null= True)
    material_used3 = models.CharField(max_length=100, blank = True, null= True)
    material_used4 = models.FloatField(default=0)
    labour1 = models.CharField(max_length=100, blank = True, null= True)
    labour2 = models.CharField(max_length=100, blank = True, null= True)
    labour3 = models.FloatField(default=0)
    optional1 = models.CharField(max_length=100, blank = True, null= True)
    optional2 = models.CharField(max_length=100, blank = True, null= True)
    optional3 = models.CharField(max_length=100, blank = True, null= True)
    optional4 = models.CharField(max_length=100, blank = True, null= True)
    optional5 = models.CharField(max_length=100, blank = True, null= True)
    optional6 = models.CharField(max_length=100, blank = True, null= True)
    optional7 = models.CharField(max_length=100, blank = True, null= True)
    optional8 = models.CharField(max_length=100, blank = True, null= True)
    optional9 = models.CharField(max_length=100, blank = True, null= True)
    optional10 = models.CharField(max_length=100, blank = True, null= True)
    optional11 = models.CharField(max_length=100, blank = True, null= True)
    mainsidesum = models.FloatField(default=0)
    materiallaboursum = models.FloatField(default=0)
    deliverypackagesum = models.FloatField(default=0)
    delivery_cost = models.FloatField(default=0)
    packaging_cost = models.FloatField(default=0)
    total_cost = models.FloatField(default=0)
    original_delivery_date = models.DateField(blank = True, null= True)
    customer_name = models.CharField(max_length=100, blank = True, null= True)
    customer_email = models.CharField(max_length=100, blank = True, null= True)
    customer_mobile = models.CharField(max_length=100, blank = True, null= True)
    # fast_shipping = models.BooleanField(default=False)
    tracking_id = models.CharField(max_length=100, blank = True, null= True)
    shipping_method = models.CharField(max_length=100, blank = True, null= True)
    address = models.CharField(max_length=100, blank = True, null= True)
    country = models.CharField(max_length=100, blank = True, null= True)
    shop = models.ForeignKey('user.User', related_name =  'shop' ,on_delete=models.DO_NOTHING, blank = True, null= True)
    revenue = models.FloatField(default=0)
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, blank = True, null= True)
    
    
    def getOrderID(self):
        return self.order_id if self.order_id else ''
    
    def get2OrderID(self):
        return self.order_id_2 if self.order_id_2 else ''
    
    def getStatus(self):
        return self.status if self.status else ''
    
    def getOrderDate(self):
        return self.order_date if self.order_date else None
    
    def getAdminPhoto(self):
        return self.admin_photo.url if self.admin_photo else ''
    
    def getManufacturerPhoto(self):
        return self.manufacturer_photo.url if self.manufacturer_photo else ''
    
    def getTitle(self):
        return self.title if self.title else ''
    
    def getQuantity(self):
        return self.quantity if self.quantity else 0
    
    def getMaterial(self):
        return self.material if self.material else ''
    
    def getColor(self):
        return self.color if self.color else ''
    
    def getSize(self):
        return self.size if self.size else ''
    
    def getPersonalization(self):
        return self.personalization if self.personalization else ''
    
    def getLastDate(self):
        return self.last_date if self.last_date else None
    
    def getMainStone1(self):
        return self.main_stone1 if self.main_stone1 else ''
    
    def getMainStone2(self):
        return self.main_stone2 if self.main_stone2 else ''
    
    def getMainStone3(self):
        return self.main_stone3 if self.main_stone3 else ''
    
    def getMainStone4(self):
        return self.main_stone4 if self.main_stone4 else 0.0
    
    def getSideStone1(self):
        return self.side_stone1 if self.side_stone1 else ''
    
    def getSideStone2(self):
        return self.side_stone2 if self.side_stone2 else ''
    
    def getSideStone3(self):
        return self.side_stone3 if self.side_stone3 else ''
    
    def getSideStone4(self):
        return self.side_stone4 if self.side_stone4 else 0.0
    
    def getMaterialUsed1(self):
        return self.material_used1 if self.material_used1 else 0.0
    
    def getMaterialUsed2(self):
        return self.material_used2 if self.material_used2 else 0.0
    
    def getMaterialUsed3(self):
        return self.material_used3 if self.material_used3 else 0.0
    
    def getMaterialUsed4(self):
        return self.material_used4 if self.material_used4 else 0.0
    
    def getLabour1(self):
        return self.labour1 if self.labour1 else ''
    
    def getLabour2(self):
        return self.labour2 if self.labour2 else ''
    
    def getLabour3(self):
        return self.labour3 if self.labour3 else 0.0
    
    def getDeliveryCost(self):
        return self.delivery_cost if self.delivery_cost else 0
    
    def getPackagingCost(self):
        return self.packaging_cost if self.packaging_cost else 0
    
    def getTotalCost(self):
        return self.total_cost if self.total_cost else 0
    
    def getOriginalDeliveryDate(self):
        return self.original_delivery_date if self.original_delivery_date else None
    
    def getCustomerName(self):
        return self.customer_name if self.customer_name else ''
    
    def getCustomerEmail(self):
        return self.customer_email if self.customer_email else ''
    
    def getCustomerMobile(self):
        return self.customer_mobile if self.customer_mobile else ''
    
    # def getFastShipping(self):
    #     return self.fast_shipping if self.fast_shipping else False
    
    def getTrackingID(self):
        return self.tracking_id if self.tracking_id else ''
    
    def getShippingMethod(self):
        return self.shipping_method if self.shipping_method else ''
    
    def getAddress(self):
        return self.address if self.address else ''
    
    def getCountry(self):
        return self.country if self.country else ''
    
    def getCompleted(self):
        return self.completed if self.completed else False

    
    def __str__(self):
        return str(self.title) + '-' + self.order_id
    
class Topup(models.Model):
    manufacturer = models.ForeignKey('user.User', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    gold = models.FloatField(default=0)
    def __str__(self):
        return str(self.manufacturer.email)
    

class ChatNote(models.Model):
    item = models.ForeignKey(Item, related_name='chat_notes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.note[:20]}'
