import streamlit as st
import language_tool_python

st.set_page_config(
    page_title="AI Grammar & Spelling Correction",
    page_icon="✍️"
)

st.title("✍️ AI Grammar & Spelling Correction")
st.write("Enter an English sentence and get the corrected version.")

# Initialize LanguageTool
tool = language_tool_python.LanguageTool("en-US")

# User input
sentence = st.text_area(
    "Enter your sentence:",
    placeholder="Example: He don't knows python."
)

# Correction button
if st.button("Correct Sentence"):
    if sentence.strip():
        corrected_sentence = tool.correct(sentence)

        st.subheader("Result")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Original Sentence**")
            st.info(sentence)

        with col2:
            st.write("**Corrected Sentence**")
            st.success(corrected_sentence)

    else:
        st.warning("Please enter a sentence.")

tool.close()