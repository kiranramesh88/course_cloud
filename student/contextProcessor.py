from student.models import Cart,Order,Wishlist

def cartCount(request):
    if request.user.is_authenticated:
        count=Cart.objects.filter(user_object=request.user).count()
        return {"cartcount":count}
    
def courseCount(request):
    if request.user.is_authenticated:
        ordercount=Order.objects.filter(student=request.user,is_paid=True).count()
        return {"courseCount":ordercount}
    return {"courseCount":0}

def wishlistCount(request):
    if request.user.is_authenticated:
        wishlistcount=Wishlist.objects.filter(user_object=request.user).count()
        return {"wishlistCount":wishlistcount}
    return {"wishlistCount":0}
