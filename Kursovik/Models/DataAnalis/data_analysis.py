import pandas as pd
from APS_project.Kursovik.Models.order.request import Request
import numpy as np


# Настройка отображения всех столбцов
pd.set_option('display.max_columns', None)  # Показывать все столбцы
pd.set_option('display.max_rows', None)     # Показывать все строки (опционально)
pd.set_option('display.width', 1000)        # Ширина вывода для удобства
pd.set_option('display.float_format', '{:.6f}'.format)  # Формат вывода чисел с плавающей точкой

class Data:
    def __init__(self, source_count, mode) -> None:
        self.data_list = pd.DataFrame.from_records([
            {
                'source_id': id,
                'generated_orders': 0,
                'refused_orders': 0,
                'refuse_probability': 0,
                'sum_order_time_in_system': 0,
                'sum_waiting_time': 0,
                'waiting_times': [],
                'sum_processing_time': 0,
                'processing_times': []
            }
            for id in range(source_count)
        ])
        self.mode = mode

    def add_generated_order(self, request: Request) -> None:
        self.data_list.at[request.get_source_id(), 'generated_orders'] += 1
        if self.mode == 'step':
            input()

    def add_refused_order(self, request: Request, sys_time: float) -> None:
        self.data_list.at[request.get_source_id(), 'refused_orders'] += 1
        self.data_list.at[request.get_source_id(), 'sum_order_time_in_system'] += sys_time - request.get_gen_time()
        self.data_list.at[request.get_source_id(), 'sum_waiting_time'] += sys_time - request.get_gen_time()
        self.data_list.at[request.get_source_id(), 'waiting_times'].append(sys_time - request.get_gen_time())

    def add_order_waiting_time(self, request: Request, sys_time: float):
        self.data_list.at[request.get_source_id(), 'sum_waiting_time'] += sys_time - request.get_gen_time()
        self.data_list.at[request.get_source_id(), 'waiting_times'].append(sys_time - request.get_gen_time())
        self.data_list.at[request.get_source_id(), 'sum_order_time_in_system'] += sys_time - request.get_gen_time()

    def add_order_processing_time(self, request: Request, processing_time: float):
        self.data_list.at[request.get_source_id(), 'sum_processing_time'] += processing_time
        self.data_list.at[request.get_source_id(), 'processing_times'].append(processing_time)
        self.data_list.at[request.get_source_id(), 'sum_order_time_in_system'] += processing_time
        if self.mode == 'step':
            input()

    def to_df(self):
        self.data_list['refuse_probability'] = self.data_list['refused_orders'] / self.data_list['generated_orders']
        self.data_list['avg_time_in_system'] = self.data_list['sum_order_time_in_system'] / self.data_list['generated_orders']
        self.data_list['avg_waiting_time'] = self.data_list['sum_waiting_time'] / self.data_list['generated_orders']
        self.data_list['avg_processing_time'] = self.data_list['sum_processing_time'] / (self.data_list['generated_orders'] - self.data_list['refused_orders'])
        self.data_list['var_waiting_times'] = self.data_list['waiting_times'].apply(lambda x: np.var(x))
        self.data_list['var_processing_times'] = self.data_list['processing_times'].apply(lambda x: np.var(x))

        if self.mode == 'step':
            df_sources = self.data_list.rename(columns={
                'source_id': 'Номер Источника',
                'generated_orders': 'Сгенерированные заявки',
                'refused_orders': 'Отказ'
            }).drop(columns=['sum_order_time_in_system', 'sum_waiting_time', 'sum_processing_time',
                             'processing_times', 'waiting_times', 'refuse_probability', 'avg_time_in_system',
                             'avg_waiting_time', 'avg_processing_time', 'var_waiting_times', 'var_processing_times'])
            return df_sources
        else:

            df_sources = self.data_list.rename(columns={
                'source_id': 'Номер Источника',
                'generated_orders': 'Сгенерированные заявки',
                'refused_orders': 'Отказ',
                'refuse_probability': 'Вероятность отказа',
                'sum_processing_time': 'Общее время обработки',
                'avg_processing_time': 'Среднее время обработки',
                'sum_waiting_time': 'Общее время ожидания',
                'avg_waiting_time': 'Среднее ожидание'

            }).drop(columns=['sum_order_time_in_system', 'waiting_times',
                             'processing_times','avg_time_in_system','var_waiting_times','var_processing_times'])
            return df_sources

