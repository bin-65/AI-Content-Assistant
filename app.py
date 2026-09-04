import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate customized posts with captions and hashtags powered by Gemini.")

# Sidebar for API Key
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook"])
        content_type = st.selectbox("Content Type", ["Informational Post", "Promotional / Ad", "Storytelling", "Short Tip / How-To"])
    
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Persuasive", "Witty & Humorous", "Inspirational"])
        target_audience = st.text_input("Target Audience", placeholder="e.g., Software Engineers, Small Business Owners")
    
    topic = st.text_area("Topic / Core Message", placeholder="What do you want to talk about?")
    
    submit_btn = st.form_submit_button("Generate Content")

# Generation Logic
if submit_btn:
    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            # Initialize Google GenAI Client
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            You are an expert social media manager. Create a complete post based on these details:
            - Platform: {platform}
            - Content Type: {content_type}
            - Tone: {tone}
            - Target Audience: {target_audience}
            - Topic: {topic}

            Format your response clearly into three sections:
            1. **Main Post Content**
            2. **Engaging Caption**
            3. **Relevant Hashtags**
            """
            
            with st.spinner("Drafting your post..."):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                )
                
            st.success("Generated successfully!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")