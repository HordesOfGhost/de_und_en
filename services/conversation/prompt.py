def get_conversation_prompt(topic: str) -> str:
    """
    Generates a conversation prompt based on the provided topic.

    Parameters
    -----------
    topic : str
        The topic for the conversation.

    Returns
    --------
    str
        The formatted conversation prompt.
    """
    prompt_template = '''
    Create a natural-sounding conversation between two or more people about {}.
    Use realistic, everyday language with a smooth, dynamic flow.
    
    Instructions:
    - Do not include any introductory or concluding remarks.
    - Do not say things like "I understand the task" or "I hope this helps". 
    
    Vary the use of:
    - **Nouns** (common, proper, abstract, collective) to add variety and context.
    - **Pronouns** (he, she, they, them, etc.), ensuring a balance of gender-neutral and diverse pronouns throughout.
    - **Verbs** (action, linking, auxiliary, modal) in various tenses (present, past, future, continuous, perfect) and voices (active, passive) to reflect different actions and states.
    - **Adjectives** (descriptive, quantitative, demonstrative) to provide details and nuance to the nouns.
    - **Adverbs** (manner, time, place, degree) to modify verbs, adjectives, or other adverbs, adding depth to the actions or qualities described.
    - **Prepositions** to show relationships between different elements in the sentence (e.g., "in," "on," "under," "between").
    - **Conjunctions** (coordinating, subordinating, correlative) to connect ideas, clauses, and sentences smoothly.
    - **Interjections** to express emotions, surprise, or reactions (e.g., "Wow!", "Oh no!").
    - **Articles** (definite and indefinite) to specify or generalize the nouns in the conversation.
    - **Tenses** (present, past, future, continuous, perfect) to convey actions or states happening at different times.
    - **Voice** (active and passive) to indicate whether the subject performs or receives the action.
    - **Mood** (indicative, imperative, subjunctive) to reflect the nature of the statements (facts, commands, wishes, etc.).
    - **Clauses** (independent, dependent, relative) to form complex sentences and provide detailed context.
    - **Punctuation** (commas, periods, exclamation marks, question marks, semicolons, colons) to structure the conversation clearly.
    - **Direct and Indirect Speech** to reflect how people communicate what others say.
    - **Conditionals** (zero, first, second, third) to express different situations, possibilities, and outcomes.

    The conversation should feel spontaneous and natural, with varied pacing, incorporating different grammatical structures to make it engaging and dynamic. Include a mix of simple and complex sentences, varied tones (e.g., excited, thoughtful, casual), and occasional shifts in perspective or tense.

    Only provide the conversation—no explanations or descriptions needed.
    Write the character's name first, followed by their dialogue. Ensure the character's name are gender-neutral.
    '''
    
    return prompt_template.format(topic)
