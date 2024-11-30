import streamlit as st
from openai import OpenAI


# Define a function to classify comments based on a specific category
def classify_comment(comment, category, client):
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
   #related_to_category = "yes" in classification_and_reason.lower().split("is this comment related to the category?")[-1].strip()
   if category.lower() == "general":
       related_to_category = True
   else:
       related_to_category = "yes" in classification_and_reason.lower().split("is this comment related to the category?")[-1].strip()


   return classification_and_reason, is_bad, related_to_category


# Streamlit app title and description
st.title("💬 Social Media Comment Classifier")
st.write(
   "This is a Comment Classifier Feature on Social media that allows you to archive bad comments "
   "based on a specific category (e.g., body, makeup, personality). "
   "To use this feature, you need an OpenAI API key."
)


# OpenAI API key input
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
   st.info("Please enter your OpenAI API key to use the app.", icon="🗝️")
else:
   client = OpenAI(api_key=openai_api_key)


   # Prompt for user to select archiving mode
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
               with st.spinner("Checking comment..."):
                   result, is_bad, _ = classify_comment(comment, "general", client)
                   if is_bad:
                       st.error("🚫 Comment Archived!")
                   else:
                       st.success("✅ Comment Kept!")
               
                   #st.write(result)


   elif archive_mode == "Customize":
       category = st.selectbox(
           "Select the type of comments to archive:",
           options=["Body", "Makeup", "Personality", "Fashion", "Performance"],
       ).lower()


       comment = st.text_input("Enter a comment:")
       if st.button("Submit Comment"):
           if comment:
               with st.spinner("Checking comment..."):
                   result, is_bad, related_to_category = classify_comment(comment, category, client)
                   if is_bad and related_to_category:
                       st.error("🚫 Comment Archived!")
                   else:
                       st.success("✅ Comment Kept!")
                   #st.write(related_to_category)
                   #st.write(result)


