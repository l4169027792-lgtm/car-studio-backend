from io import BytesIO

import streamlit as st
from PIL import Image

from image_utils import add_shadow, image_to_bytes, remove_background_from_bytes

st.set_page_config(page_title="Car Studio - Background Remover", page_icon="🚗", layout="wide")

st.title("🚗 Car Background Remover with Shadow")
st.write(
    "Upload a car photo to remove its background using **rembg** and add a soft shadow for a studio-like effect."
)

uploaded_file = st.file_uploader("Upload a car image", type=["png", "jpg", "jpeg", "webp"])


def _hex_to_rgba(hex_value: str, alpha: int = 255):
    hex_value = hex_value.lstrip("#")
    return tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4)) + (alpha,)


default_bg = "#ffffff"
default_shadow = "#000000"

col_controls1, col_controls2, col_controls3 = st.columns(3)

with col_controls1:
    blur_radius = st.slider("Shadow blur radius", min_value=5, max_value=80, value=35, step=5)

with col_controls2:
    shadow_x = st.slider("Shadow offset X", min_value=-100, max_value=100, value=45, step=5)
    shadow_y = st.slider("Shadow offset Y", min_value=-100, max_value=100, value=45, step=5)

with col_controls3:
    shadow_opacity = st.slider("Shadow opacity", min_value=0, max_value=255, value=150, step=5)
    padding = st.slider("Canvas padding", min_value=20, max_value=150, value=70, step=10)

bg_color = st.color_picker("Background color", value=default_bg)
shadow_color_hex = st.color_picker("Shadow color", value=default_shadow)

if uploaded_file:
    file_bytes = uploaded_file.read()
    original_image = Image.open(BytesIO(file_bytes)).convert("RGBA")

    with st.spinner("Removing background..."):
        no_bg_image = remove_background_from_bytes(file_bytes)

    with st.spinner("Adding shadow..."):
        shadowed_image = add_shadow(
            no_bg_image,
            shadow_offset=(shadow_x, shadow_y),
            shadow_color=_hex_to_rgba(shadow_color_hex, shadow_opacity),
            background_color=_hex_to_rgba(bg_color),
            blur_radius=blur_radius,
            padding=padding,
        )

    st.subheader("Preview")
    col1, col2, col3 = st.columns(3)
    col1.image(original_image, caption="Original", use_container_width=True)
    col2.image(no_bg_image, caption="Background Removed", use_container_width=True)
    col3.image(shadowed_image, caption="With Shadow", use_container_width=True)

    st.subheader("Download")
    col_dl1, col_dl2 = st.columns(2)
    col_dl1.download_button(
        "Download background-removed PNG",
        data=image_to_bytes(no_bg_image),
        file_name="car-no-background.png",
        mime="image/png",
    )
    col_dl2.download_button(
        "Download with shadow PNG",
        data=image_to_bytes(shadowed_image),
        file_name="car-shadow.png",
        mime="image/png",
    )
else:
    st.info("Upload a car image to start processing.")
