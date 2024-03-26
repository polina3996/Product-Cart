Dataclass 'Product' stores the information about the product and its price.

Dataclass 'Promo' stores the promocode, its discount and a list of products for discount(if it's not given - all the products in the cart can get this discount).

Instead of the database, all active promocodes are stored here in the global variable 'ACTIVE_PROMO'.

Dataclass 'Cart' gives the possibility to:
- add products into the product cart
- count the total sum of all the products in the cart(including discounts)
- apply and cancel given regular discount to all the products in the cart
- apply and cancel given promocode discount 

Besides, both discounts can't be used together. It's possible to use only the last applied discount. 

