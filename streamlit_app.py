import streamlit as st
from openai import OpenAI

# Define a function to classify comments based on a specific category
def classify_comment(comment, category, client):
    prompt = (
        f"As a TikTok comment classifier, classify comments as 'good' or 'bad' specifically in relation to '{category}'. "
        f"Also, indicate explicitly if the comment is relevant to '{category}' or not.\n\n"
        f"Comment: '{comment}'\n\n"
        "Classification and Reason:\n"
        "Is this comment related to the category? (Yes/No):"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    classification_and_reason = response.choices[0].message.content.strip()
    is_bad = "bad" in classification_and_reason.lower()
    related_to_category = "yes" in classification_and_reason.lower().split("is this comment related to the category?")[-1].strip()

    return classification_and_reason, is_bad, related_to_category

# Streamlit app for Instagram-like settings page
st.title("Instagram Settings Demo")
st.subheader("🔧 Comment Moderation Settings")

# OpenAI API key input for demo purposes
openai_api_key = st.text_input("Enter OpenAI API Key:", type="password")
if openai_api_key:
    client = OpenAI(api_key=openai_api_key)

    # Simulate "Comment Moderation" section
    st.write("**Comment Moderation Options**")
    archive_mode = st.radio(
        "Choose your comment moderation strategy:",
        ["Archive ALL bad comments", "Keep ALL Comments", "Customize"]
    )

    comment = st.text_input("Enter a comment to simulate moderation:")

    if st.button("Submit Comment"):
        if comment:
            with st.spinner("Moderating comment..."):
                if archive_mode == "Keep ALL Comments":
                    st.success("✅ Comment Kept!")
                elif archive_mode == "Archive ALL bad comments":
                    result, is_bad, _ = classify_comment(comment, "general", client)
                    if is_bad:
                        st.error("🚫 Comment Archived!")
                    else:
                        st.success("✅ Comment Kept!")
                    st.write(result)
                elif archive_mode == "Customize":
                    category = st.selectbox(
                        "Select a category to monitor:",
                        ["Body", "Makeup", "Personality", "Fashion", "Performance"]
                    ).lower()
                    result, is_bad, related_to_category = classify_comment(comment, category, client)
                    if is_bad and related_to_category:
                        st.error("🚫 Comment Archived!")
                    else:
                        st.success("✅ Comment Kept!")
                    st.write(result)

else:
    st.warning("Please enter your OpenAI API key to enable comment moderation.")
