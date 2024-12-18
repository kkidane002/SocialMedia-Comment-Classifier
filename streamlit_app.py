import streamlit as st
import openai  # Correct import
from googletrans import Translator  # No need for exceptions import
import os

# Load the OpenAI API key securely from an environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("OpenAI API key not found. Please set it as an environment variable.")
else:
    openai.api_key = openai_api_key  # Set OpenAI API key
    translator = Translator()  # Initialize the Google Translator

    # Function to translate non-English comments into English
    def translate_to_english(comment):
        try:
            # Translate using Google Translate
            translated = translator.translate(comment, src='auto', dest='en')
            return translated.text
        except Exception as e:  # Handle all general exceptions
            st.error(f"Error occurred while translating: {e}")
            return comment  # Fallback to the original comment

    # Function to classify comments based on a specific category
    def classify_comment(comment, category):
        if category.lower() == "general":
            prompt = (
                f"As a TikTok comment classifier, classify the comment as 'good' or 'bad'.\n\n"
                f"Comment: '{comment}'\n\n"
                "Classification and Reason:"
            )
        else:
            prompt = (
                f"As a TikTok comment classifier, classify comments as 'good' or 'bad' specifically in relation to '{category}'. "
                f"Also, indicate explicitly if the comment is relevant to '{category}' or not.\n\n"
                f"Comment: '{comment}'\n\n"
                "Classification and Reason:\n"
                "Is this comment related to the category? (Yes/No):"
            )

        response = openai.ChatCompletion.create(  # Correct method
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        classification_and_reason = response.choices[0].message.content.strip()

        # Determine if the comment is bad
        is_bad = any(keyword in classification_and_reason.lower() for keyword in ["bad", "offensive", "inappropriate", "harmful"])
        
        # Determine relevance for specific categories
        if category.lower() == "general":
            related_to_category = True
        else:
            relevance_part = classification_and_reason.lower().split("is this comment related to the category?")[-1].strip()
            related_to_category = "yes" in relevance_part

        return classification_and_reason, is_bad, related_to_category

    # Streamlit app title and description
    st.title("💬 Social Media Comment Classifier")
    st.write(
        "This is a Comment Classifier Feature on Social media that allows you to archive bad comments "
        "based on a specific category (e.g., body, makeup, personality)."
    )

    # User selects archiving mode
    archive_mode = st.radio(
        "Select your archiving preference:",
        ["Archive ALL bad comments", "Keep ALL Comments", "Customize"]
    )

    if archive_mode == "Keep ALL Comments":
        comment = st.text_input("Enter a comment:")
        if st.button("Submit Comment"):
            if comment:
                st.success("✅ Comment Kept!")

    elif archive_mode == "Archive ALL bad comments":
        comment = st.text_input("Enter a comment:")
        if st.button("Submit Comment"):
            if comment:
                with st.spinner("Processing comment..."):
                    # Translate the comment
                    translated_comment = translate_to_english(comment)
                    st.write(f"Translated Comment: {translated_comment}")  # Debugging

                    # Classify the translated comment
                    result, is_bad, _ = classify_comment(translated_comment, "general")
                    st.write(f"Classification Result: {result}")  # Debugging
                    
                    if is_bad:
                        st.error("🚫 Comment Archived!")
                    else:
                        st.success("✅ Comment Kept!")

    elif archive_mode == "Customize":
        category = st.selectbox(
            "Select the type of comments to archive:",
            options=["Body", "Makeup", "Personality", "Fashion", "Performance"],
        ).lower()

        comment = st.text_input("Enter a comment:")
        if st.button("Submit Comment"):
            if comment:
                with st.spinner("Processing comment..."):
                    # Translate the comment
                    translated_comment = translate_to_english(comment)
                    st.write(f"Translated Comment: {translated_comment}")  # Debugging

                    # Classify the translated comment
                    result, is_bad, related_to_category = classify_comment(translated_comment, category)
                    st.write(f"Classification Result: {result}")  # Debugging

                    if is_bad and related_to_category:
                        st.error("🚫 Comment Archived!")
                    else:
                        st.success("✅ Comment Kept!")
