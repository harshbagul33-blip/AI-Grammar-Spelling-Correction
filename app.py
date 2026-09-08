import streamlit as st
import requests

st.set_page_config(
    page_title="AI Grammar & Spelling Correction",
    page_icon="✍️"
)

st.title("✍️ AI Grammar & Spelling Correction")
st.write("Correct grammar and spelling mistakes using AI-powered language checking.")

sentence = st.text_area(
    "Enter your sentence:",
    placeholder="Example: He don't knows python."
)


def correct_sentence(sentence):
    url = "https://api.languagetool.org/v2/check"

    data = {
        "text": sentence,
        "language": "en-US"
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        return sentence

    result = response.json()

    corrected_sentence = sentence

    # Apply corrections from right to left
    for match in reversed(result["matches"]):
        offset = match["offset"]
        length = match["length"]

        if match["replacements"]:
            replacement = match["replacements"][0]["value"]

            corrected_sentence = (
                corrected_sentence[:offset]
                + replacement
                + corrected_sentence[offset + length:]
            )

    return corrected_sentence


if st.button("Correct Sentence"):

    if sentence.strip():

        corrected = correct_sentence(sentence)

        st.subheader("Result")

        st.write("**Original Sentence:**")
        st.info(sentence)

        st.write("**Corrected Sentence:**")
        st.success(corrected)

    else:
        st.warning("Please enter a sentence.")