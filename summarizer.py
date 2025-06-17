import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from heapq import nlargest

def summarize_text(text, max_length=100, min_length=30):
    """Generate extractive summary using NLTK with controlled length"""
    # Download required NLTK data if not already downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # If text is too short, return it as is
    if len(sentences) <= 3:
        return text

    # Tokenize words and remove stopwords and punctuation
    stop_words = set(stopwords.words('english') + list(punctuation))
    word_tokens = word_tokenize(text.lower())
    word_tokens = [word for word in word_tokens if word not in stop_words]

    # Calculate word frequencies
    freq_dist = FreqDist(word_tokens)
    
    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in freq_dist:
                if sentence not in sentence_scores:
                    sentence_scores[sentence] = freq_dist[word]
                else:
                    sentence_scores[sentence] += freq_dist[word]

    # Calculate number of sentences to include (approximately 20% of original)
    num_sentences = max(2, min(5, int(len(sentences) * 0.2)))
    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    
    # Sort sentences in their original order
    summary_sentences = sorted(summary_sentences, key=lambda x: sentences.index(x))
    
    # Join sentences to form summary
    summary = ' '.join(summary_sentences)
    
    # Ensure summary is not too long
    if len(summary.split()) > max_length:
        summary = ' '.join(summary.split()[:max_length]) + '...'
    
    return summary

def summarize_sections(sections):
    """Generate concise summaries for each section of the document"""
    section_summaries = []
    
    for section in sections:
        if len(section["content"]) > 50:  # Only summarize substantial sections
            # Limit section summary to 2-3 sentences
            summary = summarize_text(section["content"], max_length=50, min_length=20)
            section_summaries.append({
                "heading": section["heading"],
                "summary": summary
            })
    
    # Limit total number of sections to prevent too long summaries
    if len(section_summaries) > 5:
        # Keep the most important sections (first and last)
        important_sections = [section_summaries[0]]  # First section
        if len(section_summaries) > 1:
            important_sections.append(section_summaries[-1])  # Last section
        # Add middle sections if any
        if len(section_summaries) > 2:
            middle_index = len(section_summaries) // 2
            important_sections.append(section_summaries[middle_index])
        section_summaries = important_sections
    
    return section_summaries 