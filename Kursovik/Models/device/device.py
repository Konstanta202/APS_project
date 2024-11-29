from APS_project.Kursovik.Models.order.order import Order
from APS_project.Kursovik.Models.DataAnalis.data_analysis import Data
import random as rnd

class Device:
    id: int
    a: float
    b: float
    availability: bool
    start_handling_time: float
    finish_handling_time: float
    total_work_time: float
    order: Order
    finished_orders: int
    stats: Data

    def __init__(self, id: int, a: float, b: float, stats: Data) -> None:
        self.id = id
        self.a = a
        self.b = b
        self.availability = True
        self.total_work_time = 0
        self.finish_handling_time = 0
        self.order = None
        self.finished_orders = 0
        self.stats = stats

    def get_finish_handling_time(self):
        return self.finish_handling_time
    def get_device_id(self):
        return self.id
    def is_available(self) -> bool:
        return self.availability

    def set_order_to_handling(self, order: Order, sys_time: float) -> None:
        self.order = order
        self.start_handling_time = sys_time
        work_time = (self.b - self.a) * rnd.random() + self.a
        self.finish_handling_time = self.start_handling_time + work_time
        self.total_work_time += work_time
        self.availability = False
        if self.stats.mode == 'step':
            print(f'Поступила заявка: {order.get_id()} в прибор {self.id} в {sys_time}, время обработки {work_time}')

    def finish_handling_order(self) -> None:
        if self.stats.mode == 'step':
            print(f'Завершение обработки заявки: {self.order.get_complex_id()} в: {self.get_finish_handling_time()} прибором номер: {self.id}')
        self.finished_orders +=1
        self.stats.add_order_processing_time(self.order, self.finish_handling_time - self.start_handling_time)
        self.start_handling_time = 0
        self.finish_handling_time = 0
        self.availability = True
        self.order = None
        self.total_work_time += self.finish_handling_time - self.start_handling_time
