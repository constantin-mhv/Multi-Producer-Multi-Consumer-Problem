"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = dict()
        self.carts = dict()
        self.producers_ids = 0
        self.carts_ids = 0

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.producers_ids = self.producers_ids + 1
        return str(self.producers_ids - 1)

    def add_producer(self, producer):
        prod_id = self.register_producer()
        self.producers[prod_id] = list()
        return prod_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        # TODO: add lock publish()
        # print("publish!! ", j, product)
        prod_storage = self.producers[producer_id]
        if len(prod_storage) == self.queue_size_per_producer:
            return False
        prod_storage.append(product)
        return True

    def return_product(self, producer_id, product):
        # TODO: add lock return_product()
        prod_storage = self.producers[producer_id]
        prod_storage.append(product)

    def register_cart(self):
        # TODO: add lock register_cart() or not?
        self.carts_ids = self.carts_ids + 1
        return self.carts_ids - 1

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # TODO: add lock new_cart()
        cart_id = self.register_cart()
        self.carts[cart_id] = list()
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        # TODO: lock add_product()
        for prod_id, producer_storage in self.producers.items():
            try:
                i = producer_storage.index(product)
                bought_product = producer_storage.pop(i)
                cart = self.carts[cart_id]
                cart.append((prod_id, bought_product))
                return True
            except ValueError:
                continue

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        cart = self.carts[cart_id]
        i = 0
        for pr in cart:
            if pr[1] == product:
                break
            i = i + 1
        removed_product = cart.pop(i)
        self.return_product(removed_product[0], removed_product[1])

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        res = list()
        [res.append(cart[1]) for cart in self.carts[cart_id]]
        # print(res)
        return res

    def print_products(self, prod_id, prod_name):
        print(prod_name, end=":\n")
        prod_list = self.producers[prod_id]
        for p in prod_list:
            print(p)

    def print_all_products(self):
        for prod_id, prod in self.producers.items():
            for p in prod:
                print(prod_id, p, "size:", len(prod), end='')

        print("")
