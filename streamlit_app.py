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

    # Determine if the comment is related to the specified category
    is_bad = "bad" in classification_and_reason.lower()
    related_to_category = category.lower() in classification_and_reason.lower()

    # Format the result based on whether it’s within the selected category
    result = classification_and_reason
    if is_bad:
        if related_to_category:
            result += f"\nThis is a bad comment and is related to the '{category}' category."
        else:
            result += f"\nThis is a bad comment but is not related to the '{category}' category."
    else:
        if related_to_category:
            result += f"\nThis is a good comment and is related to the '{category}' category."
        else:
            result += f"\nThis is a good comment but is not related to the '{category}' category."

    return result


# Streamlit app title and description
st.title("💬 TikTok Comment Classifier")
st.write(
    "This is a chatbot-based app that allows you to classify TikTok comments "
    "based on a specific category (e.g., body, makeup, personality). "
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
        if not category or not comment:
            st.warning("Please provide both a category and a comment.")
        else:
            with st.spinner("Classifying comment..."):
                try:
                    result = classify_comment(comment, category, client)
                    st.success("Classification Complete!")
                    st.write(f"**Result for '{category}' comments:**")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
