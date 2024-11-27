class Config:
    def __init__(self,
                 order_count: int = 2000,
                 source_count: int = 5,
                 device_count: int = 11,
                 buffer_capacity: int = 11,
                 lambda_: float = 1.3,
                 a: float = 2,
                 b: float = round(1.5,1),
                 mode: str = 'auto') -> None:
        self.order_count = order_count
        self.source_count = source_count
        self.device_count = device_count
        self.buffer_capacity = buffer_capacity
        self.lambda_ = lambda_
        self.a = a
        self.b = b
        self.mode = mode

    def to_dict(self) -> dict:
        return self.__dict__