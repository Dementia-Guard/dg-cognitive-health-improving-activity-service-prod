import re
from difflib import SequenceMatcher
from datetime import datetime

def evaluate_question_set(answers_obj: object):
  total_score = 0.0
  for entry in answers_obj:
    question_type = entry.get("type")
    if question_type == "article":
      answer = entry.get("answer", "")
      user_input = entry.get("user_input", "")
      score = 0.0
      if answer != "" and user_input != "":
        score = calculate_score(answer, user_input)
        
      total_score = total_score + score
      
    elif question_type == "standard":
      answer = entry.get("answer", "")
      user_input = entry.get("user_input", "")
      score = 0.0
      if answer != "" and user_input != "":
        score = calculate_score(answer, user_input)
      
      total_score = total_score + score
      
    elif question_type == "date":
      question = entry.get("question")
      date_type = question.replace("What is the ", "").strip()
      
      now = datetime.now()

      current_year = now.year
      current_date = now.strftime("%Y-%m-%d")
      current_day = now.strftime("%A")
      current_week = now.strftime("%U")
      current_month = now.strftime("%B")
      current_season = get_season(now.month, now.day)
      user_input = entry.get("user_input", "")
      score=0.0
      if(date_type=="year"):
        score = calculate_score(current_year, user_input)
      elif(date_type=="date"):
        score = calculate_score(current_date, user_input)
      elif(date_type=="day"):
        score = calculate_score(current_day, user_input)
      elif(date_type=="week"):
        score = calculate_score(current_week, user_input)
      elif(date_type=="month"):
        score = calculate_score(current_month, user_input)
      elif(date_type=="season"):
        score = calculate_score(current_season, user_input)
        
      total_score = total_score + score
  return total_score
  
def get_season(month, day):
  if (month == 12 and day >= 21) or (1 <= month <= 2) or (month == 3 and day < 20):
    return "Winter"
  elif (month == 3 and day >= 20) or (month <= 5) or (month == 6 and day < 21):
    return "Spring"
  elif (month == 6 and day >= 21) or (month <= 8) or (month == 9 and day < 22):
    return "Summer"
  else:
    return "Autumn"     
  
def calculate_score(answer, user_input):
  def normalize(text):
    return re.sub(r"[^\w\s]", "", text).lower().strip()
  
  normalized_answer = normalize(answer)
  normalized_input = normalize(user_input)
  
  answer_tokens = set(normalized_answer.split())
  input_tokens = set(normalized_input.split())
    
  if normalized_input == normalized_answer:
    return 1.0

  if input_tokens & answer_tokens:
    return 0.5
  
  return 0.0