from sqlalchemy.orm import Session
from services.db.models import WritingMetaData  

def get_prompt_for_generating_writing_content(level:str, db:Session):

  recent_topics = db.query(WritingMetaData.topic)\
                      .filter(WritingMetaData.level == level)\
                      .order_by(WritingMetaData.id.desc())\
                      .limit(11)\
                      .all()

  recent_topic_list = [topic[0] for topic in recent_topics]
  recent_topics_str = ", ".join(f'"{t}"' for t in recent_topic_list) if recent_topic_list else "None"

  prompt = f"""
      You are a German language tutor creating structured language learning material.

      1. Choose a realistic and unique topic appropriate for learners in Germany.
      Avoid using any of the following recent topics for level {level}:
      [{recent_topics_str}]

      Example topics by CEFR level (only for inspiration, not limitation):

      - A1: Einkaufen im Supermarkt, Tagesablauf, Im Café, Mein Haus, Familie vorstellen, Wetter, Hobbys, Auf dem Markt, In der Schule, Tiere, Selbstvorstellung
      - A2: Urlaub in Deutschland, Ein Besuch beim Arzt, Mein Lieblingsfilm, Das Wochenende, Sport machen, Mit dem Bus fahren, Das Frühstück, Kleidung kaufen
      - B1: Digitalisierung im Alltag, Recycling und Umwelt, Schule damals und heute, Warum Lesen wichtig ist, Öffentliche Verkehrsmittel, Soziale Medien
      - B2: Work-Life-Balance, Internet und Datenschutz, Kultur und Identität, Klimawandel, Bildungsgerechtigkeit, Meinungsfreiheit
      - C1: Zukunft der Arbeit, Soziale Ungleichheit, Migration und Integration, Wissenschaft und Gesellschaft, Medienkompetenz, Bildungspolitik
      - C2: Philosophie des Glücks, Postmoderne Literatur, Neuroethik, Künstliche Intelligenz und Moral, Nachhaltige Stadtplanung, Zukunft der Demokratie

      {{
      "level": "{level}",
      "topic": "[Insert selected topic]",
      }}

      Only output valid JSON — no extra explanation, no markdown, no formatting outside of JSON.
  """
  return prompt



def get_writing_task_evaluation_prompt(topic, article, questions_and_answers, user_answers):
  prompt = "You are an expert evaluator for a German writing comprehension task.\n\n"
  prompt += "Topic: " + topic + "\n\n"
  prompt += "Article:\n" + article + "\n\n"
  prompt += "Evaluate the following question-answer pairs:\n\n"

  for i, (qa, user_answer) in enumerate(zip(questions_and_answers, user_answers), start=1):
      question = qa.get("question", "")
      correct_answer = qa.get("answer", "")
      prompt += "Question " + str(i) + ":\n"
      prompt += "Question: " + question + "\n"
      prompt += "Correct Answer: " + correct_answer + "\n"
      prompt += "User Answer: " + user_answer + "\n\n"

  prompt += """Your task is to:
            - Evaluate whether each user answer is:
            - Grammatically correct,
            - Syntactically well-formed,
            - Semantically aligned with the article and question,
            - Factually correct based on the article,
            - Complete and contextually relevant.
            - Provide a float score between 0.0 (completely incorrect) and 1.0 (fully correct).
            - Give a brief explanation for each evaluation highlighting grammatical, semantic, or contextual issues if any.

            Return your output in the following JSON format:

            {
            "explanation": [list of explanation by analyzing each user's answer],
            "score": [list of float scores for each answer]
            }
            """
  return prompt

def get_writing_evaluation_prompt(topic: str, content: str, level: str) -> str:
    prompt = f"""
You are a certified German language evaluator tasked with assessing student writing submissions.

Evaluate the following response for a CEFR level {level} writing task.

### Writing Topic:
"{topic}"

### Student's Response:
\"\"\"
{content}
\"\"\"

### Evaluation Guidelines:

- Carefully review the student's text sentence by sentence.
- Analyze grammar, syntax, vocabulary, and fluency in each sentence.
- Identify recurring mistakes or patterns of error.
- Evaluate whether the content is relevant, coherent, and contextually aligned with the topic.
- Assess whether the writing meets the expected language complexity and appropriateness for CEFR level {level}.
- Suggest improvements if necessary.

### Output Format (strict JSON only — no extra text):

Return a JSON object with:
- `"score"`: a float between 0 (poor) and 100 (excellent) indicating the overall quality.
- `"evaluation"`: a detailed paragraph summarizing grammatical quality, vocabulary usage, topic relevance, structural coherence, and CEFR-level alignment. Include improvement suggestions if applicable.

Example:
{{
  "score": 78,
  "evaluation": "The student demonstrates a good grasp of B1-level vocabulary and mostly accurate grammar. Some verb conjugation errors and incorrect article usage are present. The text remains on topic but could be improved with richer detail. Sentence variety and subordinate clause structure need work. Consider revisiting adjective endings and passive constructions."
}}
"""
    return prompt

