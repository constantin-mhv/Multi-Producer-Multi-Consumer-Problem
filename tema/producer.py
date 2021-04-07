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
        Thread.__init__(self, daemon=kwargs["daemon"])
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.prod_name = kwargs["name"]
        self.prod_id = self.marketplace.add_producer()

    def run(self):
        """
        The entry point for a thread.
        """
        i = 0
        while True:
            product_info = self.products[i]
            product = product_info[0]
            num = product_info[1]
            time_to_wait = product_info[2]
            for _ in range(num):
                while True:
                    res = self.marketplace.publish(self.prod_id, product)
                    # if product was not published, sleep
                    if not res:
                        time.sleep(self.republish_wait_time)
                    else:
                        break
                time.sleep(time_to_wait)
            i = i + 1
            # if the production plan is over, start from the beginning
            if i == len(self.products):
                i = 0
