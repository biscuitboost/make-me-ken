import streamlit as st
import requests
import io
from PIL import Image
import replicate
from streamlit_cropper import st_cropper

# Set up configurations
st.set_option('deprecation.showfileUploaderEncoding', False)

MODEL_ADDRESS = "lucataco/faceswap:9a4298548422074c3f57258c5d544497314ae4112df80d116f0d2109e843d20d"
TITLE = "I want to be Ken"
DESC = '''Upload or take a picture to become Ken or Barbie'''

def run_model(target_image_path, swap_image_data):
    output = replicate.run(
        MODEL_ADDRESS,
        input={
            "target_image": open(target_image_path, "rb"),
            "swap_image": io.BytesIO(swap_image_data)
        }
    )
    return output

def main():
    st.title(TITLE)
    st.write(DESC)

    target_image_option = st.radio('Take Your Pick:', ('Ken', 'Barbie'))
    image_file = st.file_uploader("Upload Clear Photo Of Your Face.", type=['jpg', 'png'])

    if image_file is not None:
        img = Image.open(image_file)
        realtime_update = st.checkbox(label="Crop in Real Time", value=True)

        if realtime_update:
            st.write("Double click to save crop")

        # Get a cropped image from the frontend
        cropped_img = st_cropper(img, realtime_update=realtime_update, box_color="#0000FF",
                                aspect_ratio=(1, 1))

        st.image(cropped_img, width = 512)
        buf = io.BytesIO()
        cropped_img.save(buf, format='JPEG')
        byte_im = buf.getvalue()

        if st.button("Make Me Ken"):
            if target_image_option == 'Ken':
                target_image_path = 'ken.jpg'
            else:
                target_image_path = 'barbie.jpg'

            output = run_model(target_image_path, byte_im)
            print("************************")
            print(type(output))
            print(output)
            st.image(output, width = 725)
            st.balloons()



if __name__ == '__main__':
  main()
