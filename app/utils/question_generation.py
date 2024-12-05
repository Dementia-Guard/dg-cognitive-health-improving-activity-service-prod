from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import random
import re
from ..utils.fetch_article import get_random_article

# Load the model and tokenizer of question from standards
standards_trained_model_path = "ml_models/question_generation_standards_new/t5_trained_model"
standards_trained_tokenizer_path = "ml_models/question_generation_standards_new/t5_tokenizer"

# Load the model and tokenizer of question from articles
articles_trained_model_path = "ml_models/question_generation_articles_new/t5_trained_model_articles_v1"
articles_trained_tokenizer_path = "ml_models/question_generation_articles_new/t5_tokenizer_articles_v1"

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer of question from standards once during initialization
standards_model = T5ForConditionalGeneration.from_pretrained(standards_trained_model_path).to(device)
standards_tokenizer = T5Tokenizer.from_pretrained(standards_trained_tokenizer_path)

# Load model and tokenizer of question from articles once during initialization
articles_model = T5ForConditionalGeneration.from_pretrained(articles_trained_model_path).to(device)
articles_tokenizer = T5Tokenizer.from_pretrained(articles_trained_tokenizer_path)

def generate_question_standards_model_calling(prompt: str, difficulty_level: str) -> list:
  try:
    text = f"prompt: {prompt} difficulty_level: {difficulty_level}"

    encoding = standards_tokenizer.encode_plus(
      text,
      max_length=512,
      padding="max_length",
      truncation=True,
      return_tensors="pt"
    ).to(device)

    input_ids = encoding["input_ids"]
    attention_mask = encoding["attention_mask"]

    standards_model.eval()
    beam_outputs = standards_model.generate(
      input_ids=input_ids,
      attention_mask=attention_mask,
      max_length=72,
      early_stopping=True,
      num_beams=5,
      num_return_sequences=1
    )

    output = [
      standards_tokenizer.decode(output_, skip_special_tokens=True, clean_up_tokenization_spaces=True)
      for output_ in beam_outputs
    ]

    return output

  except Exception as e:
    raise RuntimeError(f"Error in generating questions: {str(e)}")

def generate_question_articles_model_calling(context: str) -> list:
  try:
    text = f"context: {context}"

    encoding = articles_tokenizer.encode_plus(
      text,
      max_length=512,
      padding="max_length",
      truncation=True,
      return_tensors="pt"
    ).to(device)

    input_ids = encoding["input_ids"]
    attention_mask = encoding["attention_mask"]

    articles_model.eval()
    beam_outputs = articles_model.generate(
      input_ids=input_ids,
      attention_mask=attention_mask,
      max_length=72,
      early_stopping=True,
      num_beams=5,
      num_return_sequences=1
    )

    output = [
      articles_tokenizer.decode(output_, skip_special_tokens=True, clean_up_tokenization_spaces=True)
      for output_ in beam_outputs
    ]

    return output

  except Exception as e:
    raise RuntimeError(f"Error in generating questions: {str(e)}")

def generate_question_articles(difficulty_level: int) -> list:
  if difficulty_level == 1:
    article_details = get_random_article()
  elif difficulty_level == 2:
    article_details = get_random_article()
  elif difficulty_level == 3:
    article_details = get_random_article()
  else:
    article_details = get_random_article()
  
  context = article_details["text"]
  
  output = generate_question_articles_model_calling(context)
  
  result = {}
  
  try:
    question_part, answers_part = output[0].split(" answer: ", 1)
    
    question = question_part.replace("question: ", "").strip()

    result = {
      "type": "article",
      "article": context,
      "question": question,
      "answer": answers_part,
      "output": output
    }
  except Exception as e:
    print(f"Error parsing input: {e}")

  return result

def generate_question_standard(difficulty_level):
  standard_types = [
    "Memory Recall", 
    "Number Countdown", 
    "Spelling"
  ]
  
  standard_type = random.choice(standard_types)
  prompt = ""
  
  if standard_type == "Memory Recall":
    end = ["fruits", "objects", "tools", "colors", "animals"]
    prompt = "Recall words related to "+random.choice(end)+"."
  
  elif standard_type == "Number Countdown":
    start = '10'
    end = '100'
    count = '3'
    
    if (difficulty_level == 1):
      start = '10'
      end = '99'
      count = '3'
    
    elif (difficulty_level == 2):
      start = '100'
      end = '999'
      count = '5'
    
    elif (difficulty_level == 3):
      start = '1000'
      end = '2000'
      count = '7'
    
    prompt = "Count"+count+" numbers backward starting from a number in the range ("+start+","+end+")."
  
  elif standard_type == "Spelling":
    end = ["places", "objects", "animals"]
    prompt = "Spell a word related to "+random.choice(end)+" backwards."
  
  output = generate_question_standards_model_calling(prompt, str(difficulty_level))
  
  question_part, answers_part = output[0].split(" answer: ", 1)
  question = question_part.replace("question: ", "").strip()
    
  result = {
    "type": standard_type,
    "question": question,
    "answer": answers_part,
    "output": output
  }
  return result

def generate_question_date():
  questions = [
    "What is the year?",
    "What is the season?",
    "What is the date?",
    "What is the day?",
    "What is the week",
    "What is the month?"
  ]
  
  question = random.choice(questions)
  result = {
    "type": "date",
    "question": question
  }
  return result

def create_question_set(difficulty_level):
  no_of_questions = 4
  percentage_of_standard_questions = 75
  # Determine the number of questions from each function
  no_of_standard_questions = int((percentage_of_standard_questions / 100) * no_of_questions)
  no_of_article_questions = no_of_questions - no_of_standard_questions
  
  standard_questions = [
    generate_question_standard(difficulty_level)
    for _ in range(no_of_standard_questions)
  ]
  
  article_questions = [
    generate_question_articles(difficulty_level)
    for _ in range(no_of_article_questions)
  ]
  
  date_question = generate_question_date()
  
  all_questions = standard_questions + article_questions
  all_questions.append(date_question)
  random.shuffle(all_questions)

  return all_questions
