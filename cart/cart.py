from catalogue.models import ProductVariant


class Cart:

    def __init__(self, request):

        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, variant, qty=1):

        variant_id = str(variant.id)

        if variant_id not in self.cart:
            self.cart[variant_id] = qty
        else:
            self.cart[variant_id] += qty

        self.session.modified = True

    def remove(self, variant):

        variant_id = str(variant.id)

        if variant_id in self.cart:
            del self.cart[variant_id]

        self.session.modified = True

    def update_qty(self, variant, qty):

        variant_id = str(variant.id)

        self.cart[variant_id] = qty

        self.session.modified = True

    def __len__(self):

        return sum(self.cart.values())

    def clear(self):

        self.session['cart'] = {}
        self.cart = {}
        self.session.modified = True
    
    
    def __iter__(self):

        variant_ids = self.cart.keys()

        variants = ProductVariant.objects.filter(id__in=variant_ids)

        for variant in variants:

            item = {
                'variant': variant,
                'quantity': self.cart[str(variant.id)],
                'total_price':variant.price * self.cart[str(variant.id)]}

            yield item