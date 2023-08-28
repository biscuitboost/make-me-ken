import streamlit as st
import requests
import io
from PIL import Image
import replicate

# Set up configurations
st.set_option('deprecation.showfileUploaderEncoding', False)

MODEL_ADDRESS = "lucataco/faceswap:9a4298548422074c3f57258c5d544497314ae4112df80d116f0d2109e843d20d"
TITLE = "I want to be Ken"
DESC = '''Upload or take a picture to become Ken or Barbie'''

def run_model(target_image_path, swap_image_data):
    output = replicate.run(
        "lucataco/faceswap:9a4298548422074c3f57258c5d544497314ae4112df80d116f0d2109e843d20d",
        input={
            "target_image": open(target_image_path, "rb"),
            "swap_image": io.BytesIO(swap_image_data)
        }
    )
    return output

def main():
    st.title(TITLE)
    st.write(DESC)

    target_image_option = st.radio('Select your Target Image:', ('Ken', 'Barbie'))
    image_file = st.file_uploader("Upload Swap Image", type=['jpg', 'png'])

    if image_file is not None:
        image_data = image_file.read()
        st.image(image_data, width = 725)

        if st.button("Swap Face"):
            if target_image_option == 'Ken':
                target_image_path = 'ken.jpg'
            else:
                target_image_path = 'barbie.jpg'

            output = run_model(target_image_path, image_data)
            st.image(output, width = 725)

if __name__ == '__main__':
  main()
