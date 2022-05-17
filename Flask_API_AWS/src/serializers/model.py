import json
from typing import Any


class PDFJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        try:
            return {"code": str(o.code), "dest_path": o.dest_path, "extension": o.extension}
        except AttributeError:
            return super().default(0)


class JPGJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        try:
            return {"code": str(o.code), "src_path": o.src_path, "extensions": f"{list(o.extensions)}"}
        except AttributeError:
            return super().default(0)