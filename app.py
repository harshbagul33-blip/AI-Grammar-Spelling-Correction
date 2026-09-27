import streamlit as st
import language_tool_python
import textstat
import pandas as pd
import re


st.set_page_config(
    page_title="AI Grammar & Spelling Correction",
    page_icon="✍️",
    layout="wide"
)


@st.cache_resource
def load_tool():
    try:
        return language_tool_python.LanguageTool("en-US")
    except Exception:
        return None


tool = load_tool()


sample_sentences = [
    "He don't knows Python.",
    "She have completed her assignment.",
    "I am go to college every day.",
    "They was playing cricket yesterday.",
    "My friend are very helpful.",
    "I has a new laptop.",
    "We is learning artificial intelligence.",
    "He do not likes coffee.",
    "She go to market yesterday.",
    "The students was studying for exam."
]


def check_sentence_length(sentence):
    word_count = len(sentence.split())

    if word_count > 25:
        return (
            f"Long sentence ({word_count} words). "
            "Consider splitting it into two sentences."
        )

    return f"Sentence length is acceptable ({word_count} words)."


def get_readability(original, corrected):
    try:
        original_score = textstat.flesch_reading_ease(original)
        corrected_score = textstat.flesch_reading_ease(corrected)

        if corrected_score > original_score:
            result = "Improved"
        elif corrected_score < original_score:
            result = "Decreased"
        else:
            result = "No Change"

        return (
            round(original_score, 2),
            round(corrected_score, 2),
            result
        )

    except Exception:
        return None, None, "Not Available"


def correct_text(text):

    if tool is None:
        return {
            "original": text,
            "corrected": text,
            "changes": 0,
            "status": "Correction Failed",
            "original_score": None,
            "corrected_score": None,
            "readability": "Not Available",
            "sentences": [],
            "error": "LanguageTool could not be loaded."
        }

    try:

        matches = tool.check(text)

        corrected = language_tool_python.utils.correct(
            text,
            matches
        )

        changes = len(matches)

        if text.strip() == corrected.strip():
            status = "No Changes Needed"
        else:
            status = "Corrected"

        original_score, corrected_score, readability = get_readability(
            text,
            corrected
        )

        original_sentences = re.split(
            r'(?<=[.!?])\s+',
            text.strip()
        )

        sentence_results = []

        for sentence in original_sentences:

            if sentence.strip():

                sentence_results.append({
                    "Sentence": sentence,
                    "Feedback": check_sentence_length(sentence)
                })

        return {
            "original": text,
            "corrected": corrected,
            "changes": changes,
            "status": status,
            "original_score": original_score,
            "corrected_score": corrected_score,
            "readability": readability,
            "sentences": sentence_results,
            "error": None
        }

    except Exception as error:

        return {
            "original": text,
            "corrected": text,
            "changes": 0,
            "status": "Correction Failed",
            "original_score": None,
            "corrected_score": None,
            "readability": "Not Available",
            "sentences": [],
            "error": str(error)
        }


st.title("AI Grammar & Spelling Correction")

st.write("Harsh Prashant Bagul")

st.write(
    "Enter English text and check grammar, spelling, "
    "corrections and readability."
)


text = st.text_area(
    "Enter text",
    height=200,
    placeholder="Example: He don't knows Python."
)


if st.button("Correct Text", type="primary"):

    if not text.strip():

        st.warning("Please enter some text.")

    else:

        result = correct_text(text)

        st.subheader("Original")
        st.info(result["original"])

        st.subheader("Corrected")

        if result["status"] == "Correction Failed":
            st.error(result["corrected"])
        else:
            st.success(result["corrected"])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Corrections",
                result["changes"]
            )

        with col2:

            if result["original_score"] is not None:
                st.metric(
                    "Original Score",
                    result["original_score"]
                )
            else:
                st.metric(
                    "Original Score",
                    "N/A"
                )

        with col3:

            if result["corrected_score"] is not None:
                st.metric(
                    "Corrected Score",
                    result["corrected_score"]
                )
            else:
                st.metric(
                    "Corrected Score",
                    "N/A"
                )

        with col4:
            st.metric(
                "Status",
                result["status"]
            )

        st.subheader("Readability")

        st.write(result["readability"])

        if result["sentences"]:

            st.subheader("Sentence Analysis")

            for item in result["sentences"]:

                st.write(
                    f"Sentence: {item['Sentence']}"
                )

                st.write(
                    f"Feedback: {item['Feedback']}"
                )

                st.divider()

        if result["error"]:

            st.error(
                f"Error: {result['error']}"
            )


st.divider()

st.subheader("10 Sample Sentences")


if st.button("Analyze 10 Sentences"):

    results = []

    progress = st.progress(0)

    for index, sentence in enumerate(sample_sentences):

        result = correct_text(sentence)

        results.append({
            "Original": result["original"],
            "Corrected": result["corrected"],
            "Number of Changes": result["changes"],
            "Original Readability": result["original_score"],
            "Corrected Readability": result["corrected_score"],
            "Readability Result": result["readability"],
            "Status": result["status"]
        })

        progress.progress(
            (index + 1) / len(sample_sentences)
        )

    dataframe = pd.DataFrame(results)

    st.subheader("Final Results")

    st.dataframe(
        dataframe,
        width="stretch"
    )

    total_sentences = len(results)

    corrected_count = sum(
        1
        for result in results
        if result["status"] == "Corrected"
    )

    unchanged_count = sum(
        1
        for result in results
        if result["status"] == "No Changes Needed"
    )

    failed_count = sum(
        1
        for result in results
        if result["status"] == "Correction Failed"
    )

    total_corrections = sum(
        result["Number of Changes"]
        for result in results
    )

    st.subheader("Overall Result")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Total Sentences",
            total_sentences
        )

    with col2:
        st.metric(
            "Corrected",
            corrected_count
        )

    with col3:
        st.metric(
            "No Changes",
            unchanged_count
        )

    with col4:
        st.metric(
            "Failed",
            failed_count
        )

    with col5:
        st.metric(
            "Total Corrections",
            total_corrections
        )

    csv_data = dataframe.to_csv(index=False)

    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="grammar_results.csv",
        mime="text/csv"
    )