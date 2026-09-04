import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate customized posts with captions and hashtags powered by Gemini.")

# Streamlit Secrets se API key lene ka tareeqa
api_key = st.secrets.get("GEMINI_API_KEY")

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
        st.error("API Key nahi mili! Streamlit Cloud Settings > Secrets mein GEMINI_API_KEY add karein.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
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
                response = model.generate_content(prompt)
                
            st.success("Generated successfully!")
            st.markdown("---")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
