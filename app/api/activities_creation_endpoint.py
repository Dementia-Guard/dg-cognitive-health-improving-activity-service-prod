from fastapi import APIRouter, HTTPException
from newspaper import Article, Source
from pydantic import BaseModel
import random
import nltk
from ..utils.question_generation import create_question_set
from ..utils.question_evaluation import evaluate_question_set
from ..utils.q_learning import action

router = APIRouter()
user_state = {"averageScore": 0.8, "averageResponseTime": 0.6, "difficultyLevel": 2} # retrieved from database | Not implemented

class QuestionRequest(BaseModel):
  # context: str
  # answer: str
  # difficulty_level: int
  # no_of_questions: int
  # percentage_of_standard_questions: int
  user_id: str
  
class EvaluationRequest(BaseModel):
  answers: object

@router.post("/api/activities")
async def activities_creation_endpoint():
  try:
    difficulty_level = action(user_state)["difficultyLevel"]
    questions = create_question_set(difficulty_level)
    return {"questions": questions}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@router.post("/api/process")
async def evaluate_activity_endpoint(req: EvaluationRequest):
  user_state = {"averageScore": 0.8, "averageResponseTime": 0.6, "difficultyLevel": 2}
  total_time = 0
  for answer in req.answers:
    total_time += answer["responseTime"]
  score = evaluate_question_set(req.answers)
  
  session_avg_score = score / len(req.answers)
  session_avg_time = total_time / len(req.answers)
  
  new_avg_score = (user_state["averageScore"] + session_avg_score) / 2
  new_avg_time = (user_state["averageResponseTime"] + session_avg_time) / 2
  
  user_state = {"averageScore": new_avg_score, "averageResponseTime": new_avg_time, "difficultyLevel": 2}
  
  return {
    "user_state": user_state,
    "session_score": score
  }