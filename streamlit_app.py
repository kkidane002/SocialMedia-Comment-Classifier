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

    # Return the extracted details and formatted response
    return classification_and_reason, is_bad, related_to_category


# Streamlit app title and description
st.title("💬 TikTok Comment Classifier")
st.write(
    "This is a Comment CLassifier Feature on TikTok that allows you to archive TikTok comments"
    "based on a specific category (e.g., body, makeup, personality). "
    "To use this feature, you need an OpenAI API key."
)

# OpenAI API key input
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please enter your OpenAI API key to use the app.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # Dropdown menu for category selection
    category = st.selectbox(
        "Select the type of comments to archive:",
        options=["Body", "Makeup", "Personality", "Fashion", "Performance"],
    ).lower()

    # Text area for comment input
    comment = st.text_area("Enter Test Comment to Test Archieve:")

    if st.button("Classify Comment"):
        if not category or not comment:
            st.warning("Please provide both a category and a comment.")
        else:
            with st.spinner("Classifying comment..."):
                try:
                    # Get the classification result
                    result, is_bad, related_to_category = classify_comment(comment, category, client)

                    # Display appropriate message based on classification
                    if not related_to_category:
                        st.success("Comment Kept!")
                    elif not is_bad and related_to_category:
                        st.success("Comment Kept!")
                    elif not is_bad and not related_to_category:
                        st.success("Comment Kept!") 
                    elif is_bad and not related_to_category:
                        st.success("Comment Kept!")
                    elif is_bad and related_to_category:
                        st.error("Comment Archived!") # Archive only if bad and related to category
                    else:
                        st.success("Comment Kept!")

                    # Display the classification details
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")


