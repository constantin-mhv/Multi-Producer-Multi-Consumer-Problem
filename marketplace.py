"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import threading


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the
    implementation. The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue
        associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.producers = dict()
        self.carts = dict()
        self.producers_ids = 0
        self.carts_ids = 0
        self.lock = threading.Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.

        :return: id assigned to the producer
        """
        with self.lock:
            self.producers_ids = self.producers_ids + 1
        return str(self.producers_ids - 1)

    def add_producer(self):
        """
        Adds producer to the marketplace's database

        :return: id assigned to the producer
        """
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

        :returns True or False. If the caller receives False, it should wait
        and then try again.
        """
        prod_storage = self.producers[producer_id]
        if len(prod_storage) == self.queue_size_per_producer:
            return False
        prod_storage.append(product)
        return True

    def return_product(self, producer_id, product):
        """
        Returns product to the producer storage

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: product to be returned
        """
        prod_storage = self.producers[producer_id]
        prod_storage.append(product)

    def register_cart(self):
        """
        Returns an id for the new cart

        :return: cart id
        """
        with self.lock:
            self.carts_ids = self.carts_ids + 1
        return self.carts_ids - 1

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
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

        :returns True or False. If the caller receives False, it should wait
        and then try again
        """
        for prod_id, producer_storage in self.producers.items():
            try:
                # If product is in producer storage, put it in cart
                with self.lock:
                    i = producer_storage.index(product)
                    bought_product = producer_storage.pop(i)
                cart = self.carts[cart_id]
                cart.append((prod_id, bought_product))
                return True
            except ValueError:
                # Else try other producer storage
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
        # products in cart are stored as pairs (prod_id, product)
        for prod in cart:
            if prod[1] == product:
                break
            i = i + 1
        removed_product = cart.pop(i)
        self.return_product(removed_product[0], removed_product[1])

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart

        :return a list with all the products in the cart
        """
        res = list()
        _ = [res.append(cart[1]) for cart in self.carts[cart_id]]
        return res
