from datetime import datetime
from typing import List, Dict, Any, Optional

class FilterEngine:
    @staticmethod
    def filter_by_date(
        data: List[Dict[str, Any]],
        date_field: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        if not start_date and not end_date:
            return data

        try:
            sd = datetime.fromisoformat(start_date) if start_date else datetime.min
            ed = datetime.fromisoformat(end_date) if end_date else datetime.max
        except ValueError:
            return data

        filtered = []
        for item in data:
            raw_date = item.get(date_field)
            if not raw_date:
                continue
            if isinstance(raw_date, str):
                try:
                    dt = datetime.fromisoformat(raw_date)
                except ValueError:
                    continue
            elif isinstance(raw_date, datetime):
                dt = raw_date
            else:
                continue

            if sd <= dt <= ed:
                filtered.append(item)

        return filtered
