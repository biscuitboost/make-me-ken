import streamlit as st
import io
from PIL import Image
from psd_tools import PSDImage
import replicate

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
    st.write("psd_file = ", psd_file)
    #st.write("input_files = ", input_files)
    st.write("smartobject = ", smartobject)
    psd = PSDImage.open(psd_file)
    psd.composite().save('example.png')

    
    for layer in psd:
        layer_name = layer.name
        if layer_name == smartobject:
            st.write("Found smart object")
            #layer.replace_contents(input_files)
            #st.write("Replaced smart object")
        #layer_image = layer.composite()
        #layer_image.save('%s.png' % layer.name)
    
    # Find the smart object layer
    #layer = psd.smart_object_layers[smartobject]
    
    # Replace the contents of the smart object layer with the new image
    #layer.replace_contents(input_files[layer.filepath])
    
    # Save the updated PSD file
    #psd.save()

        
    
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
        byte_im = img.tobytes()

        # Check if the image is valid and not empty
        if len(byte_im) > 0:
            make_ken_button = st.sidebar.button("Make Me Ken", key='make_ken_button')
            if make_ken_button:
                if target_image_option == 'Ken':
                    target_image_path = 'ken.jpg'
                else:
                    target_image_path = 'barbie.jpg'
                output = run_model(target_image_path, byte_im)
                #output = "ken.jpg"
                #update_psd('back-to-future.psd', byte_im, '-e-doc')
                # Replacing the input image with the output image from the model
                st.header("Output Image")
                st.image(output, use_column_width=True)
                st.balloons()

if __name__ == '__main__':
    main()
