from sqlalchemy.orm import Session
from services.db.models import ReadingMetaData  

def get_prompt_for_generating_reading_content(level:str, db:Session):

  recent_topics = db.query(ReadingMetaData.topic)\
                      .filter(ReadingMetaData.level == level)\
                      .order_by(ReadingMetaData.id.desc())\
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

      2. Write a short article in German appropriate for CEFR level {level}.
      - Level A1: very basic vocabulary, present tense
      - Level A2: simple past, daily expressions
      - Level B1: opinions and cause-effect
      - Level B2: abstract ideas, arguments
      - Level C1: academic, formal expressions
      - Level C2: near-native fluency and complexity

      3. Create 11 questions in German based on the article:
      - Questions 1 to 3: Easy : simple comprehension or vocabulary
      - Questions 4 to 7: Medium : reasoning, why/how questions
      - Questions 8 to 11: Hard : inference, opinion, or rephrasing
      - Ensure the questions appear in order that matches the time flow of the article (early questions on early parts, later ones on later parts)

      4. Write the correct answer to each question in German.

      Return everything in valid JSON format like this:

      {{
      "level": "{level}",
      "topic": "[Insert selected topic]",
      "article": "[Insert full article in German]",
      "questions_and_answers": [
        {{
          "question": "...",
          "answer": "..."
        }},
        ...
      ]
      }}

      Only output valid JSON — no extra explanation, no markdown, no formatting outside of JSON.
  """
  return prompt



def get_reading_task_evaluation_prompt(topic, article, questions_and_answers, user_answers):
  prompt = "You are an expert evaluator for a German reading comprehension task.\n\n"
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
