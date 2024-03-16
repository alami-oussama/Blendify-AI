import streamlit as st
import replicate
from openai import OpenAI


client = OpenAI()


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

def translate_to_english(input_text):
    system_prompt = "You are a translator model, you will be given a prompt in any language, you task is to translate it into English. The output should be the English sentence without any added text. If it's already in English, rewrite the same prompt."
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text},
            ]
        )
    output = response.choices[0].message.content.replace(".", "")
    print(output)

    return output


def main():
    # Title of the web app
    st.title('Blendify AI')

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
    negative_prompt = st.sidebar.text_input("Enter your negative prompt (what you don't want in your images)")

    # Style selection
    style_list = ['Photographic (Default)', 'Cinematic', 'Disney Charactor', 'Digital Art', 'Fantasy art', 'Neonpunk', 'Enhance', 'Comic book', 'Lowpoly', 'Line art']
    style_name = st.sidebar.selectbox("Select Style", style_list)

    # Sliders for various configurations
    # number_of_steps = st.sidebar.slider("Number of Steps", 1, 100, 50)
    number_of_steps = 50
    # style_strength_ratio = st.sidebar.slider("Style Strength Ratio", 15, 50, 20)
    style_strength_ratio = 30
    num_outputs = st.sidebar.slider("Number of Outputs", 1, 4, 1)

    if st.sidebar.button('Generate Images'):
        if input_image is not None:
            # Translate non-English prompts to English
            prompt = translate_to_english(prompt)

            # Add trigger to the prompt
            if "img" not in prompt:
                prompt += " img"

            # Generate the output image
            output = generate_image(input_image, prompt, style_name, negative_prompt, number_of_steps, style_strength_ratio, num_outputs)

            for index, image in enumerate(output):
                # Display the output image
                st.image(image, caption=f"Generated Image {index+1}", use_column_width=True)
        else:
            st.warning("Please upload an image.")


if __name__ == "__main__":
    main()
