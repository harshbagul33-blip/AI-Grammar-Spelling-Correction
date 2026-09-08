import language_tool_python

# Initialize grammar-checking tool
tool = language_tool_python.LanguageTool("en-US")


def correct_sentence(sentence):
    """
    Correct grammar and spelling mistakes
    in a single English sentence.
    """

    corrected_sentence = tool.correct(sentence)

    print("Original Sentence :", sentence)
    print("Corrected Sentence:", corrected_sentence)
    print("=" * 60)

    return corrected_sentence


# Sample test sentences
test_sentences = [
    "He don't knows python.",
    "She are going to school.",
    "I has a new laptop.",
    "They was playing cricket.",
    "He go to office everyday."
]


# Run correction
for sentence in test_sentences:
    correct_sentence(sentence)


# Close LanguageTool
tool.close()