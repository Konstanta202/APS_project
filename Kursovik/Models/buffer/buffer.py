from APS_project.Kursovik.Models.order.order import Order
from APS_project.Kursovik.Models.buffer.buffer_cell import BufferCell
from APS_project.Kursovik.Models.DataAnalis.data_analysis import Data
import pandas as pd
import sys

class Buffer:
    buffer_cells: list[BufferCell]
    stats: Data

    def __init__(self, capacity: int, stats: Data) -> None:
        self.buffer_cells = [BufferCell(i) for i in range(capacity)]
        self.stats = stats

    def one_free_cels(self) -> bool:
        for buffer_cell in self.buffer_cells:
            if buffer_cell.is_empty():
                return True
        return False

    def is_empty(self) -> bool:
        for buffer_cell in self.buffer_cells:
            if buffer_cell.is_empty() == False:
                return False
        return True
    
    def pop_lifo_order(self) -> Order:
        earliest_time = sys.float_info.max
        for buffer_cell in self.buffer_cells:
            if buffer_cell.get_order() is not None and buffer_cell.get_order().get_gen_time() < earliest_time:
                earliest_time = buffer_cell.get_order().get_gen_time()
                buffer_cell_with_earliest_order = buffer_cell
        return buffer_cell_with_earliest_order.pop_order()


    def pop_old_order(self) -> Order:
        earliest_time = 0.0
        for buffer_cell in self.buffer_cells:
            if buffer_cell.get_order() is not None and buffer_cell.get_order().get_gen_time() > earliest_time:
                earliest_time = buffer_cell.get_order().get_gen_time()
                buffer_cell_with_earliest_order = buffer_cell
        return buffer_cell_with_earliest_order.pop_order()



    def get_orders(self) -> Order:
        time_orders = 0.0
        for i in range(len(self.buffer)):
            if self.buffer[i] is not None and self.buffer[i].when_take_in_buffer > time_orders:
                time_orders = self.buffer[i].when_take_in_buffer
        if time_orders > 0.0:
            for i in range(len(self.buffer)):
                if self.buffer[i] is not None and self.buffer[i].when_take_in_buffer == time_orders:
                    order = self.buffer[i]
                    self.buffer[i] = None
                    return order
    
    def take_order_in_buffer(self, order: Order, sys_time):
        if self.is_empty():
            self.buffer_cells[0].set_order(order)
            if self.stats.mode == 'step':
                print(f'В буффер поступила заявка {order.get_id()}, источником: {order.get_source_id()} в ячейку : {self.buffer_cells[0].get_id()}')
            return 
        if self.one_free_cels():
            for buffer_cell in self.buffer_cells:
                if buffer_cell.is_empty():
                    buffer_cell.set_order(order)
                    if self.stats.mode == 'step':
                        print(f'Поступила заявка {order.get_id()}, источником: {order.get_source_id()} в ячейку номер: {buffer_cell.get_id()}')
                    return
        else:
            popped_order = self.pop_old_order()
            self.stats.add_refused_order(popped_order, sys_time)
            if self.stats.mode == 'step':
                print(f'Отказ заявки номер: {popped_order.get_id()}, источником: {popped_order.get_source_id()}')
            for buffer_cell in self.buffer_cells:
                if buffer_cell.is_empty():
                    buffer_cell.set_order(order)
                    if self.stats.mode == 'step':
                        print(f'Поступила заявка {order.get_id()}, источником: {order.get_source_id()}, в ячейку буфера: {buffer_cell.get_id()}')
                        
    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame.from_records(buffer_cell.__dict__ for buffer_cell in self.buffer_cells)
        df['order'] = df['order'].apply(lambda order: order.get_complex_id() if order is not None else None)
        df_buffer = df.rename(columns={
            'id': 'Номер ячейки',
            'order': 'Заявка',
            'time_in_buffer': 'Время в буфере'
        })
        return df_buffer