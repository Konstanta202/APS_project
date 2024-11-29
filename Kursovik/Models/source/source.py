from APS_project.Kursovik.Models.order.order import Order
from APS_project.Kursovik.Models.DataAnalis.data_analysis import Data
from math import log
from random import random

class Source:
    id: int
    lambda_: float
    prev_time_gen: float
    generated_order_count: int = 0
    stats: Data

    def __init__(self, id: int, lambda_: float, stats: Data) -> None:
        self.id = id
        self.lambda_ = lambda_
        self.prev_time_gen = 0.0
        self.stats = stats

    def generate_order(self) -> Order:
        self.prev_time_gen += (-1/self.lambda_) * log(random())
        order = Order(self.generated_order_count, self.id, self.prev_time_gen)
        self.generated_order_count += 1 
        return order
    
    def get_id(self) -> int:
        return self.id
