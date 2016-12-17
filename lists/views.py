import json
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static

from lists.models import WishList, Product
from lists.forms import ProductForm
from lists.scraper import get_thumbnail_urls


class ListsIndexPage(View): 
    template_name = 'lists/index.html'
    
    @method_decorator(login_required)
    def get(self, request): 
        user = request.user
        
        context = {
            'lists' : WishList.objects.filter(owner=user).order_by('-pk')
        }
        
        return render(request, self.template_name, context)


class ListPage(View): 
    template_name = 'lists/list.html'
    
    @method_decorator(login_required)
    def post(self, request, id=None): 
        if id is None: 
            raise Http404

        id = int(id)
        wishlist = get_object_or_404(WishList, id=id)
        
        postData = request.POST
        response_data = []
        
        try: 
            data_edit = postData['edit']
            data_id = postData['datid']
            data_value = postData['dvalue']
        except KeyError: 
            return ":("

        data_id = int(data_id)

        if data_edit == 'list-name': 
            wishlist.name = data_value
            wishlist.save()
            response_data = ['OK']

        elif data_edit == 'item-name': 
            product = get_object_or_404(Product, id=data_id)
            product.name = data_value
            product.save()
            response_data = ['OK']

        elif data_edit == 'item-price': 
            product = get_object_or_404(Product, id=data_id)
            product.price = Decimal(data_value[1:])
            product.save()
            response_data = ['OK']

        elif data_edit == 'item-notes': 
            product = get_object_or_404(Product, id=data_id)
            product.notes = data_value
            product.save()
            response_data = ['OK']

        return HttpResponse(
            json.dumps(response_data), 
            content_type="application/json"
        )
        

    def get(self, request, id=None): 
        if id is not None: 
            id = int(id)
            wishlist = get_object_or_404(WishList, id=id)
    
            if wishlist.private and wishlist.owner != request.user: 
                raise Http404
            
            context = {
                'wishlist' : wishlist, 
                'items' : Product.objects.filter(wishlist=wishlist).order_by('-pk')
            }
            
            if wishlist.owner != request.user: 
                context['readonly'] = True
                
            return render(request, self.template_name, context)
            
        else: 
            raise Http404
            
            
class AddList(View): 
    template_name = 'lists/index_list.html'
    
    @method_decorator(login_required)
    def post(self, request): 
        postData = request.POST
        
        try: 
            wishlist_name = postData['name']
        except KeyError: 
            return HttpResponseBadRequest("Something went wrong...")
        
        wishlist = WishList(
            name=wishlist_name, 
            owner=request.user)
        wishlist.save()
        
        context = {
            'item'  :   wishlist,
        }
        
        return render(request, self.template_name, context)
        
        
class DeleteList(View): 
    
    @method_decorator(login_required)
    def post(self, request): 
        postData = request.POST
        
        try: 
            wishlist_id = postData['wid']
        except KeyError: 
            return HttpResponseBadRequest("Something went wrong...")
            
        WishList.objects.filter(id=wishlist_id).delete()
        
        return HttpResponse("Okay!", content_type="text/plain")
        
        
class AddProduct(View): 
    template_name = 'lists/list_product.html'
    
    @method_decorator(login_required)
    def post(self, request, id=None): 

        if id is None: 
            raise Http404
            
        # We need to copy the request.POST QueryDict, because otherwise the 
        # QueryDict would be immutable, which means we wouldn't be able to 
        # correct it to contain a full URL when the 'item_thumbnail' field is 
        # set to use the default thumbnail.
        postData = request.POST.copy()
        
        try:
            item_thumbnail = postData['item_thumbnail']
        except KeyError:
            return HttpResponseBadRequest("Bad request!")
            
        defaultThumbnail = static('imgs/thumbnail_default.png')
        
        if item_thumbnail == defaultThumbnail:
            postData['item_thumbnail'] = request.build_absolute_uri(
                defaultThumbnail
            )
            
        productForm = ProductForm(postData, auto_id=True)
        
        if not productForm.is_valid():
            return HttpResponseBadRequest("Bad request!")
            
        cleanedData = productForm.cleaned_data
        
        wishlist = get_object_or_404(WishList, id=id)
        
        product = Product(
            name=cleanedData['item_name'], 
            notes=cleanedData['item_description'], 
            link=cleanedData['item_link'], 
            price=cleanedData['item_price'], 
            thumbnail=cleanedData['item_thumbnail'], 
            wishlist=wishlist,
        )
        product.save()
        
        context = {
            'item'      :   product,
            'readonly'  :   wishlist.owner != request.user,
        }
        
        return render(request, self.template_name, context)
        
        
class DeleteProduct(View): 

    @method_decorator(login_required)
    def post(self, request, id=None): 
        postData = request.POST
        
        try: 
            product_id = postData['pid']
        except KeyError: 
            return HttpResponse("Something went wrong...", content_type="text/plain")

        # We shouldn't need to worry about what list it's in. 
        # No two Products will ever have the same id.
        Product.objects.filter(id=product_id).delete()
        
        return HttpResponse("Okay!", content_type="text/plain")

    
class GetThumbnails(View):

    def post(self, request):
        try:
            url = request.POST['url']
        except KeyError:
            return HttpResponseBadRequest("Bad request!")
            
        urls = get_thumbnail_urls(url)
        
        return HttpResponse(json.dumps(urls), content_type='application/json')
        
        
