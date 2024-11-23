import streamlit as st
from openai import OpenAI

# Define a function to classify comments based on a specific category
def classify_comment(comment, category, client):
    prompt = (
        f"As a TikTok comment classifier, focus on classifying '{category}' comments.\n"
        f"Please determine if the following comment is 'good' or 'bad' in relation to '{category}', and provide a reason:\n\n"
        f"Comment: '{comment}'\n\n"
        "Classification and Reason:"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    # Extract the response
    classification_and_reason = response.choices[0].message.content.strip()

    # Determine if the comment is bad and related to the selected category
    is_bad = "bad" in classification_and_reason.lower()
    related_to_category = category.lower() in classification_and_reason.lower()

    return classification_and_reason, is_bad, related_to_category


# Streamlit app title and description
st.title("💬 TikTok Comment Classifier")
st.write(
    "This app uses AI to classify TikTok comments based on a specific category "
    "(e.g., body, makeup, personality). Archive or keep comments based on their classification. "
    "To use this app, you need an OpenAI API key."
)

# OpenAI API key input
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please enter your OpenAI API key to use the app.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Dropdown menu for category selection
    category = st.selectbox(
        "Select the type of comments to classify:",
        options=["Body", "Makeup", "Personality", "Fashion", "Performance"],
    ).lower()

    # Text area for comment input
    comment = st.text_area("Enter the comment to classify:")

    if st.button("Classify Comment"):
        if not category or not comment.strip():
            st.warning("Please provide both a category and a comment.")
        else:
            with st.spinner("Classifying comment..."):
                try:
                    # Get the classification result
                    result, is_bad, related_to_category = classify_comment(comment, category, client)

                    # Determine action based on conditions
                    if is_bad and related_to_category:
                        st.error("🚫 Comment Archived!")
                        action = "Archived"
                    else:
                        st.success("✅ Comment Kept!")
                        action = "Kept"

                    # Display the detailed classification
                    st.write("### Classification Details:")
                    st.write(f"- **Comment**: {comment}")
                    st.write(f"- **Category**: {category.capitalize()}")
                    st.write(f"- **Action**: {action}")
                    st.write(f"- **Reason**: {result}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
