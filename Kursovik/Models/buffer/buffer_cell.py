from typing import Optional
from APS_project.Kursovik.Models.order.request import Request

class BufferCell:
    id: int
    request: Optional[Request]

    def __init__(self, id: int) -> None:
        self.id = id
        self.request = None


    def set_order(self, order: Request) -> None:
        self.request = order

    def pop_order(self) -> Request:
        order_to_pop = self.request
        self.request = None
        return order_to_pop
    
    def is_empty(self) -> bool:
        return self.request is None

    def get_order(self) -> Request:
        return self.request
    
    def get_id(self) -> int:
        return self.id