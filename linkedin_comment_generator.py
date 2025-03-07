import openai
import streamlit as st
import os

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is set in Streamlit Cloud

def generate_comments(post_text, tone):
    """Generates multiple AI-powered LinkedIn comments based on the given post and tone."""
    prompt = f"Generate three {tone} LinkedIn comments for the following post:\n{post_text}\n\n1.\n2.\n3."
    
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that helps generate professional LinkedIn comments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Adjusts creativity level
            max_tokens=150
        )
        comments = response.choices[0].message.content.split("\n")
        return [comment.strip() for comment in comments if comment.strip() and not comment.strip().isdigit()]
    except Exception as e:
        return [f"Error generating comments: {str(e)}"]

# Streamlit Web App
st.title("LinkedIn Comment Generator")

post_input = st.text_area("Paste the LinkedIn post content here:")

tone = st.selectbox("Select Comment Tone:", ["Professional", "Casual", "Engaging", "Humorous"])

if st.button("Generate Comments"):
    if post_input:
        comments = generate_comments(post_input, tone.lower())
        st.subheader("Suggested Comments:")
        for i, comment in enumerate(comments, 1):
            st.write(f"**{i}.** {comment}")
    else:
        st.warning("Please enter a LinkedIn post to generate comments.")
