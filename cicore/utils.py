import base64
import io
from functools import lru_cache

import qrcode
from django.urls import reverse


@lru_cache(maxsize=32)
def make_qr_code_data_uri(url: str) -> str:
    qr_img = qrcode.make(url, border=1)
    bio = io.BytesIO()
    qr_img.save(bio, format="png")
    b64 = base64.b64encode(bio.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def reverse_absolute(request, view_name: str, **kwargs):
    url = reverse(view_name, kwargs=kwargs)
    if request:
        url = request.build_absolute_uri(url)
    return url
