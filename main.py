import streamlit as st
import replicate


def generate_image(input_image, prompt, style_name, negative_prompt, num_steps, style_strength_ratio, num_outputs):
    output = replicate.run(
        "tencentarc/photomaker:ddfc2b08d209f9fa8c1eca692712918bd449f695dabb4a958da31802a9570fe4",
        input={
            "prompt": prompt,
            "num_steps": num_steps,
            "style_name": style_name,
            "input_image": input_image,
            "num_outputs": num_outputs,
            "guidance_scale": 5,
            "negative_prompt": negative_prompt,
            "style_strength_ratio": style_strength_ratio
        }
    )
    print(output)

    return output


def main():
    # Title of the web app
    st.title('Image Generation UI')

    # Sidebar for inputs
    st.sidebar.header('Input Options')

    # Main input image
    input_image = st.sidebar.file_uploader("Upload your image", type=['jpg', 'png'], key='main_image')

    # # Optional input images
    # input_image2 = st.sidebar.file_uploader("Optional Image 2", type=['jpg', 'png'], key='image2')
    # input_image3 = st.sidebar.file_uploader("Optional Image 2", type=['jpg', 'png'], key='image3')
    # input_image4 = st.sidebar.file_uploader("Optional Image 2", type=['jpg', 'png'], key='image4')

    # Text input for prompt and negative prompt
    prompt = st.sidebar.text_input("Enter your prompt")
    if "img" not in prompt:
        prompt += " img"
    negative_prompt = st.sidebar.text_input("Enter your negative prompt")

    # Style selection
    style_list = ['Photographic (Default)', 'Cinematic', 'Disney Charactor', 'Digital Art', 'Fantasy art', 'Neonpunk', 'Enhance', 'Comic book', 'Lowpoly', 'Line art']
    style_name = st.sidebar.selectbox("Select Style", style_list)

    # Sliders for various configurations
    # number_of_steps = st.sidebar.slider("Number of Steps", 1, 100, 50)
    number_of_steps = 50
    # style_strength_ratio = st.sidebar.slider("Style Strength Ratio", 15, 50, 20)
    style_strength_ratio = 20
    num_outputs = st.sidebar.slider("Number of Outputs", 1, 4, 1)

    if st.sidebar.button('Generate Image'):
        if input_image is not None:
            # Generate the output image
            output = generate_image(input_image, prompt, style_name, negative_prompt, number_of_steps, style_strength_ratio, num_outputs)

            for image in output:
                # Display the output image
                st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.warning("Please upload an image.")


if __name__ == "__main__":
    main()
