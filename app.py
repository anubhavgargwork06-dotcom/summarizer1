from flask import Flask, render_template, request, jsonify
from gensim import corpora, models
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import string

# Download NLTK data (only first time)
nltk.download('punkt', quiet=True)

app = Flask(__name__)

# -------------------------------
#   TF-IDF SUMMARIZATION LOGIC
# -------------------------------
def tfidf_summarize(text, num_sentences=3):
    sentences = sent_tokenize(text)

    if len(sentences) <= num_sentences:
        return text

    stop_chars = set(string.punctuation)
    tokenized_sentences = []

    for sent in sentences:
        words = word_tokenize(sent.lower())
        words = [w for w in words if w not in stop_chars]
        tokenized_sentences.append(words)

    dictionary = corpora.Dictionary(tokenized_sentences)
    corpus = [dictionary.doc2bow(sent) for sent in tokenized_sentences]

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    sentence_scores = []
    for doc in corpus_tfidf:
        if not doc:
            sentence_scores.append(0)
            continue
        score = sum(weight for _, weight in doc) / len(doc)
        sentence_scores.append(score)

    top_indices = sorted(
        sorted(range(len(sentence_scores)),
               key=lambda i: sentence_scores[i],
               reverse=True)[:num_sentences]
    )

    summary = " ".join(sentences[i] for i in top_indices)
    return summary


# -------------------------------
#             ROUTES
# -------------------------------

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "Empty request"}), 400

        text = data.get("text", "").strip()
        num_sentences = int(data.get("num_sentences", 3))

        if not text:
            return jsonify({"error": "No text provided"}), 400

        summary = tfidf_summarize(text, num_sentences)
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
