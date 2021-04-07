"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class ProductInfo:
    def __init__(self, product_tuple):
        self.product = product_tuple[0]
        self.num = product_tuple[1]
        self.time_to_wait = product_tuple[2]

    def produce_one(self):
        self.num = self.num - 1

    def finished_work(self):
        if self.num == 0:
            return True
        else:
            return False


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
        # Thread.__init__(self, daemon=False)
        self.products = products
        # for p in products:
        #     self.products.insert(0, ProductInfo(p))
        self.copy_products = self.products.copy()
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.prod_name = kwargs["name"]
        self.prod_id = self.marketplace.add_producer(self)

    def run(self):
        i = 0
        k = -1
        while True:
            k = k + 1
            # if k == 6:
            #     break
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
            if i == len(self.products):
                i = 0
        # self.marketplace.print_products(self.prod_id, self.prod_name)
