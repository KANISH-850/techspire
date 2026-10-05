from typing import Optional

class PaginationParams:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit

class DateFilterParams:
    def __init__(self, start_date: Optional[str] = None, end_date: Optional[str] = None):
        self.start_date = start_date
        self.end_date = end_date
