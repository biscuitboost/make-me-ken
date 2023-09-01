import streamlit as st
import io
from PIL import Image, ImageDraw, ImageFont
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
# add text to image
################
def add_text_to_image(image_path, text, bottom_margin=10, side_margin=10):
    # Load image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate text area - 25% of image height from the bottom
    text_area_height = height * 0.25

    # Load a font
    # Here we use a default font. Adjust the path and font name according to your requirements.
    font_size = int(text_area_height) - 2 * bottom_margin  # size of font dependent on text area height
    font = ImageFont.truetype('arial.ttf', font_size)

    # Initiate draw instance
    draw = ImageDraw.Draw(image)

    # Calculate text width and height
    w, h = draw.textsize(text, font=font)

    # Calculate x position (center text)
    x_pos = (width - w) / 2

    # Calculate y position (text starts from bottom 25% and includes bottom_margin)
    y_pos = (height - text_area_height) + (text_area_height - h) / 2

    # Add text to image
    draw.text((x_pos, y_pos), text, font=font, align='center')

    # Save the image in the same format
    image.save('output.' + image.format)

    return 'Text added to image successfully!'
    
################
# Main function
################
def main():
    st.sidebar.title(TITLE)
    st.sidebar.write(DESC)

    target_image_option = st.sidebar.radio('Take Your Pick:', ('Ken', 'Barbie'))
    image_file = st.sidebar.file_uploader("Upload Clear Photo Of Your Face.", type=['jpg', 'png'])
    
    if image_file is not None:
        image_data = image_file.read()
        st.image(image_data, width = 100)

        # Check if the image is valid and not empty
        if len(image_data) > 0:
            make_ken_button = st.sidebar.button("Make Me Ken", key='make_ken_button')
            if make_ken_button:
                if target_image_option == 'Ken':
                    target_image_path = 'images/ken.jpg'
                else:
                    target_image_path = 'images/barbie.jpg'
                output = run_model(target_image_path, image_data)
                #output = "ken.jpg"
                # Replacing the input image with the output image from the model
                st.image(output, use_column_width=True)
                st.balloons()

if __name__ == '__main__':
    main()
