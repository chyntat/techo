import openai


def get_text_tags(text):
    openai.api_key = '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'
    prompt_list = [
        "What emotions are expressed in the text, give the emotions as a list : ",
        "what sentiments did the author express? give the outcome on a scale of good, neutral and bad: ",
        "Identify if any products like brands, equipment, appliences, tools, etc. are mentioned in the text. If yes, list them out: ",
        "Identify high level tags in the current text, and list them out: ",
        ""
    ]
    tags = []
    for prompt in prompt_list:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt + '\n\n' + text,
            temperature=0.7,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=1
        )
        tags_response = response.choices[0].text
        tags_response = tags_response.split('\n')
        tags.extend(tags_response)
    return tags
