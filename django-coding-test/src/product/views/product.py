from django.views import generic

from product.models import Variant, Product, ProductVariant, ProductVariantPrice
from django.core.paginator import Paginator
from django.db.models import Q


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
class AllProductView(generic.TemplateView):
    model = Product
    template_name = 'products/list.html'
    # context_object_name = "product_list"
    # paginate_by = 2
    # page_kwarg = 'product'


    def get_context_data(self, **kwargs):
        context = super(AllProductView, self).get_context_data(**kwargs)
        product = Product.objects.all()
        # productvariant = ProductVariant.objects.filter(Q(variant__title__icontains = 'Color') & Q(variant_title__gt = 1)).values('variant_title')
        
        productvariantcolor = list(set(ProductVariant.objects.filter(variant__title__icontains = 'Color').values_list("variant_title", flat = True)))
        productvariantsize = list(set(ProductVariant.objects.filter(variant__title__icontains = 'Size').values_list("variant_title", flat = True)))
        productvariantstyle = list(set(ProductVariant.objects.filter(variant__title__icontains = 'Style').values_list("variant_title", flat = True)))

        paginator = Paginator(product, 3)
        page = self.request.GET.get('page')
        paged_products = paginator.get_page(page)

        search = self.request.GET.get('title', None)
        if search:
            paged_products = product.filter(title__icontains = search)

        variant = self.request.GET.get('variant', None)
        if variant:
            paged_products = product.filter(productvariant__variant_title__icontains = variant)

        if 'price_from' in self.request.GET:    
            filter_price1 = self.request.GET.get('price_from', None)
            filter_price2 = self.request.GET.get('price_to', None)
            if filter_price1 =='':
                filter_price1=0
            else:
                paged_products = Product.objects.filter(productvariantprice__price__range=(filter_price1,filter_price2))

        date = self.request.GET.get('date', None)
        if date:
            paged_products = product.filter(created_at__icontains = date)

        context['product'] = paged_products
        context['productvariantcolor'] = productvariantcolor
        context['productvariantsize'] = productvariantsize
        context['productvariantstyle'] = productvariantstyle
        context['product_count'] = len(product)
        
        return context
