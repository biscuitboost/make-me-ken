import streamlit as st
import io
import os
import urllib
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
    
dropdown_options = {
    'Ken': 'I\'m Ken!',
    'Barbie': 'I\'m Barbie!',
    'Superman': 'I\'m Superman!',
    'Wonder Woman': 'I\'m Wonder Woman!'
}

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
def add_text_to_image(image_url, text, text_color='white', bottom_margin=25, side_margin=50):
    # Download the image from the URL and save it locally
    image_path = 'temp.jpg'
    urllib.request.urlretrieve(image_url, image_path)

    # Load image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate text area - 25% of image height from the bottom
    text_area_height = height * 0.25

    # Load a font
    # Here we use a default font. Adjust the path and font name according to your requirements.
    font_size = int(text_area_height) - 2 * bottom_margin  # size of font dependent on text area height
    font = ImageFont.truetype('Bartex.ttf', font_size)

    # Initiate draw instance
    draw = ImageDraw.Draw(image)

    # Calculate text width and height
    w, h = draw.textsize(text, font=font)

    if w < width - 2 * side_margin and h < text_area_height:
        # Text fits within the available space, no need to resize
        x_pos = side_margin  # Set x_pos to side_margin
        y_pos = (height - text_area_height) + (text_area_height - h) // 2
    else:
        # Text doesn't fit, resize the font to fit the available space
        font_size = min(font_size, int(text_area_height * (width - 2 * side_margin) / w))
        font = ImageFont.truetype('Bartex.ttf', font_size)
        w, h = draw.textsize(text, font=font)
        x_pos = side_margin  # Set x_pos to side_margin
        y_pos = (height - text_area_height) + (text_area_height - h) // 2

    # Add text to image with side margins
    draw.text((x_pos, y_pos), text, font=font, fill=text_color, align='center')

    output_path = 'output.' + image.format
    image.save(output_path)

    # Cleanup: Delete the temporary image file
    os.remove(image_path)

    return output_path


    
################
# Main function
################
def main():
    st.sidebar.title(TITLE)
    st.sidebar.write(DESC)

    target_image_option = st.sidebar.selectbox('Take Your Pick:', list(dropdown_options.keys()))
    image_file = st.sidebar.file_uploader("Upload Clear Photo Of Your Face.", type=['jpg', 'png'])
    default_text = dropdown_options[target_image_option]
    additional_text = st.sidebar.text_input('Additional Text', default_text)
    text_color = st.sidebar.color_picker("Text Color", "#ffffff")
    
    if image_file is not None:
        image_data = image_file.read()
        st.image(image_data, width=100)

        # Check if the image is valid and not empty
        if len(image_data) > 0:
            make_ken_button = st.sidebar.button("Make Me Ken", key='make_ken_button')
            if make_ken_button:
                target_image_path = 'images/' + target_image_option.lower() + '.jpg'
                st.write(target_image_path)
                replicate_output = run_model(target_image_path, image_data)
                # save output image url to local
                output_with_text = add_text_to_image(replicate_output, additional_text, text_color)
                #st.image(output_with_text, use_column_width=True)
                st.image(output_with_text, width=480)
                st.balloons()

if __name__ == '__main__':
    main()
