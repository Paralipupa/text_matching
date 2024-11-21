import pymorphy2
from fuzzywuzzy import fuzz

from typing import List, Tuple

def analize(text_list_a: List[str], text_list_b: List[str]) -> List[Tuple[str, str, int, int]]: # type: ignore
    """
    Analyze the given texts and return list of tuples where each tuple contains:

    * original text from list_a (string)
    * best matching text from list_b (string)
    * index of best matching text in list_b (int)
    * similarity score of best matching text (int)
    """
    morph_analyzer = pymorphy2.MorphAnalyzer()

    def lemmatize(text: str) -> str:
        """
        Lemmatize the given text.

        :param text: string
        :return: lemmatized string
        """
        words = text.split()
        lemmatized_words = [morph_analyzer.parse(word)[0].normal_form for word in words]
        return " ".join(lemmatized_words)

    # Iterate over each text in list_a
    for text_a in text_list_a:
        # Lemmatize the current text
        lemmatized_a = lemmatize(text_a)

        # Initialize variables to store the best match
        highest_score = 0
        best_match_b = ""
        best_match_index = -1

        # Iterate over each text in list_b
        for index_b, text_b in enumerate(text_list_b):
            # Lemmatize the current text
            lemmatized_b = lemmatize(text_b)

            # Calculate similarity score of two lemmatized strings
            similarity_score = fuzz.ratio(lemmatized_a, lemmatized_b)

            # Check if the current similarity score is higher than the highest score
            if highest_score < similarity_score:
                # Update the highest score and the best match
                highest_score = similarity_score
                best_match_b = text_b
                best_match_index = index_b

        # Yield tuple with original text from list_a, best matching text from list_b,
        # index of best matching text in list_b and similarity score of best matching text
        yield (text_a, best_match_b, best_match_index, highest_score)


def get_text():
    """
    Return two lists of texts for analysis.
    """
    # List of texts for comparison
    a = ["мама", "мыла", "раму", "Мама мыла раму", "Мамина моет рамы"]

    # List of sentences
    b = [
        "человек развивает свой ум",
        "мама любит котят",
        "мама ремонтирует раму",
        "папа моет рамы",
        "мама установила приложение",
    ]

    return a, b


if __name__ == "__main__":
    texts = get_text()
    for items in analize(*texts):
        print(f"{items[0]} - {items[1]} ({items[2]}) :  {items[3]}%")
