from fastapi import APIRouter, HTTPException
from newspaper import Article, Source
import random
import nltk

import spacy
import re
from spacy import displacy
from spacy.matcher import PhraseMatcher

news_sources = [
  "https://www.bbc.com",
  "https://www.reuters.com",
  "https://www.nytimes.com",
  "https://www.theguardian.com",
  "https://www.aljazeera.com",
  "https://www.cnn.com"
]

def get_random_article():
  try:
    # Select a random news source
    selected_source = random.choice(news_sources)
    source = Source(selected_source)

    # Build the source and fetch articles
    source.build()
    articles = source.articles

    if not articles:
      raise HTTPException(status_code=404, detail="No articles found.")

    # Select a random article
    random_article = random.choice(articles)
    random_article.download()
    random_article.parse()

    # Article details
    article_details = {
      "title": random_article.title,
      "author": random_article.authors,
      "publish_date": random_article.publish_date.isoformat() if random_article.publish_date else None,
      "source": selected_source,
      "url": random_article.source_url,
      "text": random_article.text
    }

    return article_details

  except Exception as e:
    print(f"Error fetching article: {e}")
    raise HTTPException(status_code=500, detail="Failed to fetch a valid article.")
  
# MIN_ARTICLE_LENGTH = 200
def get_selected_random_article(MIN_ARTICLE_LENGTH, MAX_ARTICLE_LENGTH):
  try:
    attempts = 0  # Counter to limit the number of attempts to find a valid article
    while attempts < 5:  # Limit to 5 attempts to find a valid article
      # Select a random news source
      selected_source = random.choice(news_sources)
      source = Source(selected_source)

      # Build the source and fetch articles
      source.build()
      articles = source.articles

      if not articles:
        raise HTTPException(status_code=404, detail="No articles found.")

      # Select a random article
      random_article = random.choice(articles)
      random_article.download()
      random_article.parse()

      # Check if the article text meets the minimum length requirement
      article_length = len(random_article.text)
      if MIN_ARTICLE_LENGTH <= article_length <= MAX_ARTICLE_LENGTH:
        # Article details
        article_details = {
          "title": random_article.title,
          "author": random_article.authors,
          "publish_date": random_article.publish_date.isoformat() if random_article.publish_date else None,
          "source": selected_source,
          "url": random_article.source_url,
          "text": random_article.text
        }
        return article_details
      else:
        attempts += 1  # Increment attempts if the article is too short

    # If no valid articles were found after several attempts
    raise HTTPException(status_code=404, detail="No valid articles found after multiple attempts.")

  except Exception as e:
    print(f"Error fetching article: {e}")
    raise HTTPException(status_code=500, detail="Failed to fetch a valid article.")

def get_today_random_article():
  return get_random_article()

def get_word_from_today_random_article():
  article_details = get_random_article()

  nlp = spacy.load("en_core_web_sm")
  
  def extract_info(text):
    doc = nlp(text)
    
    # List of specific phrases or word parts to search for
    phrases = ["Zimbabwe court", "five years in prison or a fine", "June 16", "Harare", "Citizens Coalition for Change"]
    
    # Initialize PhraseMatcher and add patterns to it
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(phrase) for phrase in phrases]
    matcher.add("PHRASES", None, *patterns)
    
    # Find all matching phrases
    matches = matcher(doc)
    
    # Extract matched phrase parts
    matched_phrases = []
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_phrases.append(span.text)
    
    # Extract named entities (e.g., persons, dates, organizations, etc.)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Filter only relevant entities (like dates, locations, organizations)
    relevant_entities = [entity for entity in entities if entity[1] in ['GPE', 'DATE', 'ORG']]
    
    return matched_phrases, relevant_entities
  
  # Extract specific information
  matched_phrases, relevant_entities = extract_info(article_details["text"])
  
  relevent_entity = relevant_entities[0]
  
  return {"matched_phrases":matched_phrases, "relevant_entities":relevent_entity[0], "text": article_details["text"]}