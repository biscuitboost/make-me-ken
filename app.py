import streamlit as st
import requests
import io
from PIL import Image
from psd_tools import PSDImage
import replicate
from streamlit_cropper import st_cropper

# Set up configurations
st.set_option('deprecation.showfileUploaderEncoding', False)

################
# Global variables
################
MODEL_ADDRESS = "lucataco/faceswap:9a4298548422074c3f57258c5d544497314ae4112df80d116f0d2109e843d20d"
TITLE = "I want to be Ken"
DESC = '''Upload or take a picture to become Ken or Barbie'''

################
# Update PSD with smart objects
# Inputs: PSD file, input file, smart object
# Outputs: new updated psd
################
def update_psd(psd_file, input_files, smartobject):
    with PSDImage.open(psd_file) as psd:
        if hasattr(psd, 'layers'):
            for layer in psd.layers:
                print("layer.name = ", layer.name")
                if layer.name == smartobject:
                    # Get the embedded smart object path
                    embedded_path = layer.smart_object.file.reference.filename
                    print("embedded_path = ", embedded_path)
                    # Check if the embedded smart object is a psd file
                    if embedded_path in input_files:
                        # Replace the embedded smart object with the input file
                        layer.smart_object.file = input_files[embedded_path]
            # save the updated psd file
            psd.save('back-to-future2.psd')
        
    
################
# Swap Face Model
################
def run_model(target_image_path, swap_image_data):
    output = replicate.run(
        MODEL_ADDRESS,
        input={
            "target_image": open(target_image_path, "rb"),
            "swap_image": io.BytesIO(swap_image_data)
        }
    )
    return output
    
################
# Main function
################
def main():
    st.sidebar.title(TITLE)
    st.sidebar.write(DESC)

    target_image_option = st.sidebar.radio('Take Your Pick:', ('Ken', 'Barbie'))
    image_file = st.sidebar.file_uploader("Upload Clear Photo Of Your Face.", type=['jpg', 'png'])

    if image_file is not None:
        img = Image.open(image_file)

        
        #realtime_update = st.sidebar.checkbox(label="Crop in Real Time", value=True)
        #if realtime_update:
        #    st.sidebar.write("Double click to save crop")
        realtime_update = True
        col1, col2 = st.columns(2)

        with col1:
            # Get a cropped image from the frontend
            cropped_img = st_cropper(img, realtime_update=realtime_update, box_color="#0000FF",
                                    aspect_ratio=(1, 1))
        
        with col2:
            st.image(cropped_img, width = 256)
            buf = io.BytesIO()
            cropped_img.save(buf, format='JPEG')
            byte_im = buf.getvalue()

        if st.button("Make Me Ken"):
            if target_image_option == 'Ken':
                target_image_path = 'ken.jpg'
            else:
                target_image_path = 'barbie.jpg'
            #output = run_model(target_image_path, byte_im)
            output = "ken.jpg"
            #update_psd('back-to-future.psd', 'blah.jpg', '-e-doc')
            # Replacing the cropped image with the output image from the model
            with col2:
                st.header("Output Image")
                st.image(output, width = 256)
            st.balloons()


if __name__ == '__main__':
  main()
