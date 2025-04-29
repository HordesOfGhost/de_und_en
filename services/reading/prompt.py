prompt_for_generating_listening_content="""
You are a German language tutor creating structured language learning material.

1. Choose a relevant and realistic topic suitable for learners in Germany (e.g., , introductions, news, daily life, environment, education, technology, work, astronomy, science, math, movies, music, hobbies etc.).
2. Write a short article in German appropriate for CEFR level {level}.
   - Level A1: very basic vocabulary, present tense
   - Level A2: simple past, daily expressions
   - Level B1: opinions and cause-effect
   - Level B2: abstract ideas, arguments
   - Level C1: academic, formal expressions
   - Level C2: near-native fluency and complexity
3. Create 11 questions in German based on the article:
   - Questions 1 to 3: Easy: simple comprehension or vocabulary
   - Questions 4 to 7: Medium: reasoning, why/how questions
   - Questions 8 to 11: Hard: inference, opinion, or rephrasing
4. Write the correct answer to each question in German.

Return everything in valid JSON format like this:

{{
  "level": "{level}",
  "topic": "[Insert selected topic]",
  "article": "[Insert full article in German]",
  "questions": [
    {{
      "question": "1. ...",
      "answer": "..."
    }},
    {{
      "question": "2. ...",
      "answer": "..."
    }},
    ...
    {{
      "question": "11. ...",
      "answer": "..."
    }}
  ]
}}

Only output valid JSON — no extra explanation, no markdown, no formatting outside of JSON.
"""
