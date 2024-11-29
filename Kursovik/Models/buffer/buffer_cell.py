from typing import Optional
from APS_project.Kursovik.Models.order.order import Order

class BufferCell:
    id: int
    order: Optional[Order]

    def __init__(self, id: int) -> None:
        self.id = id
        self.order = None

    def set_order(self, order: Order) -> None:
        self.order = order

    def pop_order(self) -> Order:
        order_to_pop = self.order
        self.order = None
        return order_to_pop
    
    def is_empty(self) -> bool:
        return self.order is None

    def get_order(self) -> Order:
        return self.order
    
    def get_id(self) -> int:
        return self.id