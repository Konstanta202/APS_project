class Request:
    id: int
    source_id: int
    gen_time: float

    def __init__(self, id: int, source_id: int, gen_time: float) -> None:
        self.id = id
        self.source_id = source_id
        self.gen_time = gen_time

    def get_id(self) -> int:
        return self.id
    
    def get_source_id(self) -> int:
        return self.source_id
    
    def get_gen_time(self) -> float:
        return self.gen_time

    def get_complex_id(self) -> tuple[int]:
        return (self.get_source_id(), self.get_id())
    def get_order_tuple_id(self) -> tuple[int]:
        return (self.get_id())

