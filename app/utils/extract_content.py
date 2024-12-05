from transformers import pipeline

def extract_useful_content(article: str) -> str:
    """
    Extracts useful content from the given article using a BERT-based summarization model.

    Parameters:
        article (str): The text of the article to summarize.

    Returns:
        str: The summarized useful content of the article.
    """
    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    
    # Generate the summary
    summary = summarizer(article, max_length=150, min_length=40, do_sample=False)
    
    # Return the summarized content
    return summary[0]['summary_text']

# Example usage
article_text = """
Artificial intelligence (AI) is transforming various industries, including healthcare, finance, and education. 
AI-powered systems are improving diagnostics in healthcare, enabling personalized medicine, and enhancing drug discovery. 
In finance, AI algorithms are optimizing trading strategies, detecting fraud, and providing customer insights. 
Education is also experiencing a revolution with AI-driven personalized learning platforms that adapt to students' needs.
"""
useful_content = extract_useful_content(article_text)
print("Useful Content:")
print(useful_content)
