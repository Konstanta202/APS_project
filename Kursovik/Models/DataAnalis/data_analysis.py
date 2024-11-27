import pandas as pd
from Kursovik.Models.order.order import Order
import numpy as np


# Настройка отображения всех столбцов
pd.set_option('display.max_columns', None)  # Показывать все столбцы
pd.set_option('display.max_rows', None)     # Показывать все строки (опционально)
pd.set_option('display.width', 1000)        # Ширина вывода для удобства
pd.set_option('display.float_format', '{:.6f}'.format)  # Формат вывода чисел с плавающей точкой

class Data:
    def __init__(self, source_count, mode) -> None:
        self.source_list_statistics_df = pd.DataFrame.from_records([
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

    def add_generated_order(self, order: Order) -> None:
        self.source_list_statistics_df.at[order.get_source_id(), 'generated_orders'] += 1
        if self.mode == 'step':
            input()

    def add_refused_order(self, order: Order, sys_time: float) -> None:
        self.source_list_statistics_df.at[order.get_source_id(), 'refused_orders'] += 1
        self.source_list_statistics_df.at[order.get_source_id(), 'sum_order_time_in_system'] += sys_time - order.get_gen_time()
        self.source_list_statistics_df.at[order.get_source_id(), 'sum_waiting_time'] += sys_time - order.get_gen_time()
        self.source_list_statistics_df.at[order.get_source_id(), 'waiting_times'].append(sys_time - order.get_gen_time())

    def add_order_waiting_time(self, order: Order, sys_time: float):
        self.source_list_statistics_df.at[order.get_source_id(), 'sum_waiting_time'] += sys_time - order.get_gen_time()
        self.source_list_statistics_df.at[order.get_source_id(), 'waiting_times'].append(sys_time - order.get_gen_time())
        self.source_list_statistics_df.at[order.get_source_id(), 'sum_order_time_in_system'] += sys_time - order.get_gen_time()

    def add_order_processing_time(self, order: Order, processing_time: float):
        self.source_list_statistics_df.at[order.get_source_id(), 'sum_processing_time'] += processing_time
        self.source_list_statistics_df.at[order.get_source_id(), 'processing_times'].append(processing_time)
        self.source_list_statistics_df.at[order.get_source_id(), 'sum_order_time_in_system'] += processing_time
        if self.mode == 'step':
            input()

    def to_df(self):
        self.source_list_statistics_df['refuse_probability'] = self.source_list_statistics_df['refused_orders'] / self.source_list_statistics_df['generated_orders']
        self.source_list_statistics_df['avg_time_in_system'] = self.source_list_statistics_df['sum_order_time_in_system'] / self.source_list_statistics_df['generated_orders']
        self.source_list_statistics_df['avg_waiting_time'] = self.source_list_statistics_df['sum_waiting_time'] / self.source_list_statistics_df['generated_orders']
        self.source_list_statistics_df['avg_processing_time'] = self.source_list_statistics_df['sum_processing_time'] / (self.source_list_statistics_df['generated_orders'] - self.source_list_statistics_df['refused_orders'])
        self.source_list_statistics_df['var_waiting_times'] = self.source_list_statistics_df['waiting_times'].apply(lambda x: np.var(x))
        self.source_list_statistics_df['var_processing_times'] = self.source_list_statistics_df['processing_times'].apply(lambda x: np.var(x))

        if self.mode == 'step':
            df_sources = self.source_list_statistics_df.rename(columns={
                'source_id': 'Номер Источника',
                'generated_orders': 'Сгенерированные заявки',
                'refused_orders': 'Отказ'
            }).drop(columns=['sum_order_time_in_system', 'sum_waiting_time', 'sum_processing_time',
                             'processing_times', 'waiting_times', 'refuse_probability', 'avg_time_in_system',
                             'avg_waiting_time', 'avg_processing_time', 'var_waiting_times', 'var_processing_times'])
            return df_sources
        else:

            df_sources = self.source_list_statistics_df.rename(columns={
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

