import base64
import io
from functools import lru_cache

import qrcode


@lru_cache(maxsize=32)
def make_qr_code_data_uri(url: str) -> str:
    qr_img = qrcode.make(url, border=1)
    bio = io.BytesIO()
    qr_img.save(bio, format="png")
    b64 = base64.b64encode(bio.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"
