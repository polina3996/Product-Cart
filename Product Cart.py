from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: float = field(repr=False)


@dataclass
class Promo:
    code: str
    code_discount: int
    product_list: list = field(default_factory=list)


@dataclass
class Cart:
    cart: list = field(default_factory=list)  # [products]
    summa: float = field(init=False, default=0) # total sum
    discount: (int, float) = field(init=False, default=0)  # applied discount
    code_discount: (int, float) = field(init=False, default=0)  # applied promocode discount
    last_disc: bool = False # whether the last applied discount was a regular discount
    last_code: bool = False  # whether the last applied discount was a promocode discount

    def add_product(self, product, amount: int = 1):
        """Adds products to 'self.cart' list; increases the total sum"""
        for i in range(amount):
            self.cart.append(product)
            self.summa += product.price

    def get_total(self):
        """Returns the total sum"""
        return self.summa

    def apply_discount(self, discount: int):
        """Applies a regular discount. If promocode discount was applied a step before, cancels it"""
        if isinstance(discount, int) and discount in range(1, 101) and self.summa > 0:
            if self.last_code:
                self.cancel_promo()
            self.discount = discount / 100
            self.summa -= self.summa * self.discount
            self.last_disc = True
        else:
            raise ValueError('Неправильное значение скидки')

    def cancel_discount(self):
        """Cancels a regular discount. Total sum returns to the value a step before"""
        self.summa = self.summa / (1 - self.discount)
        self.last_disc = False

    def apply_promo(self, code: str):
        """Applies a promocode (if it exists in the list 'ACTIVE_PROMO' below).
        If a regular discount was applied a step before, cancels it.
        To the promocode correspond promocode discount and sometimes a list of products.
        If the list is not given - promocode spreads on all the products in the cart"""
        for promo in ACTIVE_PROMO:
            if code == promo.code:
                if isinstance(promo.code_discount, int) and promo.code_discount in range(1, 101):
                    if self.last_disc:
                        self.cancel_discount()
                    self.code_discount = promo.code_discount / 100
                    if promo.product_list:
                        products_for_promo_sum = 0  # sum for promocode discount
                        for prod1 in promo.product_list: # products for promocode discount
                            for prod2 in self.cart: # compare to the products in the cart
                                if prod1 == prod2:
                                    products_for_promo_sum += prod1.price
                        self.summa -= (self.code_discount * products_for_promo_sum)
                    else:
                        self.summa -= self.summa * self.code_discount
                    self.last_code = True
                    print(f"Промокод {code} успешно применился")
                    break
        else:
            print(f"Промокода {code} не существует")

    def cancel_promo(self):
        """Cancels a promocode discount. Total sum returns to the value a step before"""
        self.summa = self.summa / (1 - self.code_discount)
        self.last_code = False


book = Product('Книга', 100.0)
usb = Product('Флешка', 50.0)
pen = Product('Ручка', 10.0)

ACTIVE_PROMO = [
    Promo('new', 20, [pen]),
    Promo('all_goods', 30),
    Promo('sale', 50, [book, usb]),
]

cart = Cart()
cart.add_product(book, 10)
cart.add_product(pen)
cart.add_product(book, 5)
cart.add_product(usb, 5)
cart.add_product(usb, 15)
cart.add_product(pen, 2)

print(cart.get_total())

# Применение промокода в 50% на книги и флешки
cart.apply_promo('sale')
print(cart.get_total())