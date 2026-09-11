import streamlit as st
import requests
import pandas as pd
import textstat

st.set_page_config(
    page_title="AI Grammar & Spelling Correction",
    page_icon="✍️"
)

st.title("✍️ AI Grammar & Spelling Correction")
st.write("Grammar correction with readability analysis.")


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
# Readability Function
# -------------------------------------------------

def readability_score(sentence):
    """Calculate the Flesch Reading Ease score."""

    return round(textstat.flesch_reading_ease(sentence), 2)


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
# Process All Sentences
# -------------------------------------------------

if st.button("Run Grammar & Readability Analysis"):

    results = []

    for i, sentence in enumerate(sample_sentences, start=1):

        # Grammar correction
        corrected, correction_count = correct_sentence(sentence)

        # Readability scores
        original_score = readability_score(sentence)
        corrected_score = readability_score(corrected)

        # Check improvement
        if corrected_score > original_score:
            readability_status = "Improved"
        elif corrected_score < original_score:
            readability_status = "Decreased"
        else:
            readability_status = "No Change"

        results.append({
            "No.": i,
            "Original Sentence": sentence,
            "Corrected Sentence": corrected,
            "Corrections": correction_count,
            "Original Readability": original_score,
            "Corrected Readability": corrected_score,
            "Readability": readability_status
        })

    # Create DataFrame
    df = pd.DataFrame(results)

    # Display results
    st.subheader("Before / After Comparison")

    st.dataframe(
        df,
        use_container_width=True
    )

    # Summary
    total_corrections = int(df["Corrections"].sum())
    improved = int((df["Readability"] == "Improved").sum())
    decreased = int((df["Readability"] == "Decreased").sum())
    no_change = int((df["Readability"] == "No Change").sum())

    st.subheader("Analysis Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Sentences", len(sample_sentences))
    col2.metric("Corrections", total_corrections)
    col3.metric("Improved", improved)
    col4.metric("No Change", no_change)

    st.write(f"**Readability improved:** {improved} sentences")
    st.write(f"**Readability decreased:** {decreased} sentences")
    st.write(f"**Readability unchanged:** {no_change} sentences")