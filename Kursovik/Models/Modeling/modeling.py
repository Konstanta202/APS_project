from APS_project.Kursovik.Models.source.source_list import SourceList
from APS_project.Kursovik.Models.device.device_list import DeviceList
from APS_project.Kursovik.Models.buffer.buffer import Buffer
from APS_project.Kursovik.Models.DataAnalis.data_analysis import Data
from math import log
from random import random
import warnings
warnings.filterwarnings("ignore")


class Modeling:
    def __init__(self, config: dict):
        self.config = config
        self.sys_time = 0
        self.stats = Data(config['source_count'], config['mode'])
        self.source_list = SourceList(config['source_count'], config['lambda_'], self.stats)
        self.device_list = DeviceList(config['device_count'], config['a'], config['b'], self.stats)
        self.buffer = Buffer(config['buffer_capacity'], self.stats)
        self.order_list = [source.generate_order() for source in self.source_list.source_list]
        self.generated_orders = 0

    def auto_simulation(self):
        while self.generated_orders < self.config['order_count']:
            self.process_req()

        while not self.device_list.are_all_available() or not self.buffer.is_empty():
            self.sys_time += (-1 / self.config['lambda_']) * log(random())
            self.device_list.manage_finished_devices(self.sys_time + 0.5)
            self.process_buffer()

        print(self.stats.to_df())

    def step_simulation(self):
        while self.generated_orders < self.config['order_count']:
            print('=' * 80)
            self.print_status()
            self.process_req()
            input()

        while not self.device_list.are_all_available() or not self.buffer.is_empty():
            self.sys_time += (-1 / self.config['lambda_']) * log(random())
            self.device_list.manage_finished_devices(self.sys_time + 0.5)
            self.process_buffer()
            print('=' * 80)
            self.print_status()
            input()

        print(self.stats.to_df())

    def process_req(self):
        print('Календарь событий:')
        for order in self.order_list:
            print(
                f"Генерация заявки: источник {order.get_source_id()}, заявка №{order.get_id()}, время генерации {order.get_gen_time():.2f}")
        for device in self.device_list.device_list:
            print(
                f'Прибор номер: {device.get_device_id()}, состояние: {device.availability}'
            )
        for buffer in self.buffer.buffer_cells:
            print(
                f'Номер ячейки буфера: {buffer.id}, состояние: {buffer.is_empty()}'
            )
        earliest_order = self.order_list.pop(self.order_list.index(min(self.order_list, key=lambda x: x.gen_time)))
        self.stats.add_generated_order(earliest_order)
        self.generated_orders += 1
        self.sys_time = earliest_order.get_gen_time()

        # Вывод информации о генерации заявки
        source_id = earliest_order.get_source_id()
        order_number = self.generated_orders
        gen_time = earliest_order.get_gen_time()
        if self.stats.mode == 'step':
            print('Выбор Заявки с наименьшим временем:')
            print(f"Генерация заявки: источник {source_id}, заявка №{order_number}, время генерации {gen_time:.2f}")

        self.device_list.manage_finished_devices(self.sys_time)

        if self.buffer.is_empty() and self.device_list.has_available_devices():
            self.device_list.set_order(earliest_order, self.sys_time)
        elif not self.device_list.has_available_devices():
            self.buffer.take_order_in_buffer(earliest_order, self.sys_time)
        else:
            self.process_buffer()
            if self.device_list.has_available_devices():
                self.device_list.set_order(earliest_order, self.sys_time)
            else:
                self.buffer.take_order_in_buffer(earliest_order, self.sys_time)

        self.order_list.append(self.source_list.get_source_by_id(earliest_order.get_source_id()).generate_order())

    def process_buffer(self):
        while not self.buffer.is_empty() and self.device_list.has_available_devices():
            first_order_in_buffer = self.buffer.pop_lifo_order()
            self.device_list.set_order(first_order_in_buffer, self.sys_time)
            self.stats.add_order_waiting_time(first_order_in_buffer, self.sys_time)

    def print_status(self):
        print(f'Время: {self.sys_time}')
        print(f'Источники:\n {self.stats.to_df()}')
        print(f'Список приборов:\n{self.device_list.to_df()}')
        print(f'Буфер:\n{self.buffer.to_df()}')


