import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="AI Grammar & Spelling Correction",
    page_icon="✍️"
)

st.title("✍️ AI Grammar & Spelling Correction")
st.write("Grammar and spelling correction using LanguageTool.")

# -------------------------------------------------
# Grammar Correction Function
# -------------------------------------------------

def correct_sentence(sentence):
    """Correct grammar and spelling in one sentence."""

    url = "https://api.languagetool.org/v2/check"

    data = {
        "text": sentence,
        "language": "en-US"
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        return sentence, 0

    result = response.json()

    corrected_sentence = sentence
    correction_count = len(result["matches"])

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

    return corrected_sentence, correction_count


# -------------------------------------------------
# 10 Sample Sentences
# -------------------------------------------------

sample_sentences = [
    "He don't knows python.",
    "She are going to school.",
    "I has a new laptop.",
    "They was playing cricket.",
    "He go to office everyday.",
    "I am learn Python programming.",
    "She have completed the project yesterday.",
    "The informations are very useful.",
    "We was working on AI project.",
    "This software have many error."
]


# -------------------------------------------------
# Process All 10 Sentences
# -------------------------------------------------

if st.button("Run Grammar Analysis"):

    results = []

    for i, sentence in enumerate(sample_sentences, start=1):

        corrected, correction_count = correct_sentence(sentence)

        results.append({
            "No.": i,
            "Original Sentence": sentence,
            "Corrected Sentence": corrected,
            "Corrections": correction_count
        })

    # Create DataFrame
    df = pd.DataFrame(results)

    # Display table
    st.subheader("Before / After Comparison")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Total corrections
    total_corrections = df["Corrections"].sum()

    st.subheader("Analysis Summary")

    st.write(f"**Total Sentences:** {len(sample_sentences)}")
    st.write(f"**Total Corrections:** {total_corrections}")