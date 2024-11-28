from APS_project.Kursovik.Models.device.device import Device
from APS_project.Kursovik.Models.order.request import Request
from APS_project.Kursovik.Models.DataAnalis.data_analysis import Data
import pandas as pd

class DeviceList:
    device_list: list[Device]
    stats: Data

    def __init__(self, device_count: int, a: float, b: int, stats: Data) -> None:
        self.device_list = [Device(i, a, b, stats) for i in range(device_count)]
        self.stats = stats

    def has_available_devices(self) -> bool:
        for device in self.device_list:
            if device.is_available():
                return True
        return False
    
    def get_first_available_device(self) -> Device:
        if self.has_available_devices():
            for device in self.device_list:
                if device.is_available():
                    return device

    def are_all_available(self) -> bool:
        for device in self.device_list:
            if device.is_available() == False:
                return False
        return True

    def set_order(self, order: Request, sys_time: float) -> None:
        self.get_first_available_device().set_order_to_handling(order, sys_time)
    
    def manage_finished_devices(self, sys_time: float) -> None:
        for device in sorted(self.device_list, key=lambda device: device.get_finish_handling_time()):
            if device.is_available() == False and device.get_finish_handling_time() < sys_time:
                device.finish_handling_order()



    def get_usage_rate(self, sys_time):
        df = self.to_df()
        df['usage_rate'] = df['total_work_time'] / sys_time
        return df.loc[:,['id', 'usage_rate']]
    
    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame.from_records(device.__dict__ for device in self.device_list)
        df['order'] = df['order'].apply(lambda order: order.get_complex_id() if order is not None else None)

        df_devices = df.rename(columns={
            'id': 'Прибор',
            'availability': 'Пуст',
            'finish_handling_time': 'Конец работы',
            'order': 'Заявка',
            'finished_orders': 'Обработанных заявок',
            'start_handling_time': 'Поступление на прибор'
        }).drop(columns=['stats', 'a', 'b', 'total_work_time'])
        return df_devices

    