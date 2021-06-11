"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are
        passed to the Thread's __init__()
        """
        Thread.__init__(self)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.cons_name = kwargs["name"]

    def run(self):
        """
        The entry point for a thread.
        """
        carts = list()
        for cart in self.carts:
            card_id = self.marketplace.new_cart()
            carts.append(card_id)
            for operation in cart:
                for _ in range(operation["quantity"]):
                    if operation["type"] == "add":
                        while True:
                            res = self.marketplace. \
                                add_to_cart(card_id, operation["product"])
                            # If it fails to add the product to cart, wait
                            if not res:
                                time.sleep(self.retry_wait_time)
                            else:
                                break
                    elif operation["type"] == "remove":
                        self.marketplace. \
                            remove_from_cart(card_id, operation["product"])
        # Printing all purchased products
        for cart_id in carts:
            cart = self.marketplace.place_order(cart_id)
            for product in cart:
                print(self.cons_name, "bought", product)
