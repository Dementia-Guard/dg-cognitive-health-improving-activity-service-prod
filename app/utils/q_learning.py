def action(state: object):
  average_response_time = state["averageResponseTime"]
  average_score = state["averageScore"]
  
  difficulty_level = state['difficultyLevel']
  if average_score < 0.5 and average_response_time > 0.8:
    difficulty_level = max(1, difficulty_level - 1)
  elif average_score > 0.7 and average_response_time < 0.5:
    difficulty_level = min(3, difficulty_level + 1)
  
  state = {"averageScore": average_score, "averageResponseTime": average_response_time, "difficultyLevel": difficulty_level}
  return state