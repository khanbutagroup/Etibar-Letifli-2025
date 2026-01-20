from decimal import Decimal
from main.models import Book, CartQuantityDiscount


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, book, quantity=1, update_quantity=False):
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {
                'quantity': 0,
                'price': str(book.price)
            }

        if update_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)

        for book in books:
            item = self.cart[str(book.id)]
            item['book'] = book
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    # ================== YENİ FUNKSİYALAR ==================

    def get_total_quantity(self):
        """Səbətdəki cəmi məhsul sayı"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_cart_discount_percent(self):
        """Cəmi məhsul sayına görə endirim"""
        total_quantity = self.get_total_quantity()

        discount = CartQuantityDiscount.objects.filter(
            min_quantity__lte=total_quantity,
            max_quantity__gte=total_quantity,
            is_active=True
        ).order_by('-discount_percent').first()

        return discount.discount_percent if discount else 0

    def get_subtotal_price(self):
        """Endirimsiz cəmi məbləğ"""
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def get_total_price(self):
        """ENDİRİMLİ yekun məbləğ"""
        subtotal = self.get_subtotal_price()
        discount_percent = self.get_cart_discount_percent()

        if discount_percent:
            discount_amount = subtotal * Decimal(discount_percent) / Decimal(100)
            return subtotal - discount_amount

        return subtotal

    def get_discount_amount(self):
        subtotal = self.get_subtotal_price()
        discount_percent = self.get_cart_discount_percent()

        if discount_percent:
            return subtotal * Decimal(discount_percent) / Decimal(100)

        return Decimal('0')

    def clear(self):
        del self.session['cart']
        self.save()
