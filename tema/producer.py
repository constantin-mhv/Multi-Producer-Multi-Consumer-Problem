"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        # Thread.__init__(self)
        Thread.__init__(self, daemon=kwargs["daemon"])
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.prod_name = kwargs["name"]
        self.prod_id = self.marketplace.add_producer(self)

    def run(self):
        while True:
            product_tuple = self.products[len(products - 1)]
            res = self.marketplace.publish(self.prod_id, product_tuple[0])
            # if product was not published, sleep
            if not res:
                time.sleep(self.republish_wait_time)
            else:
                product_tuple[1] = product_tuple[1] - 1
                time_to_wait = product_tuple[2]
                # if product was published and there are no more elements of
                # this type, remove this tuple from list
                if product_tuple[1] == 0:
                    products = products[:-1]
                # rest after hard work
                time.sleep(time_to_wait)


