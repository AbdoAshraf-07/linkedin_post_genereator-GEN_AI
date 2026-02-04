from llm_helper import llm
from few_shot import FewShotPosts
from typing import Optional

few_shot = FewShotPosts()


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    # prompt = prompt.format(post_topic=tag, post_length=length_str, post_language=language)

    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt


def edit_post(original_post: str, instruction: str, length: Optional[str] = None, language: Optional[str] = None, tag: Optional[str] = None):
    """Ask the LLM to edit the given post according to the user's instruction.

    Optional parameters can be provided to keep the edited post aligned with length/language/topic.
    """
    # Build a clear editing prompt
    prompt = f"Edit the following LinkedIn post according to the instructions.\n\nInstructions: {instruction}\n\nOriginal post:\n{original_post}\n\n"
    if tag:
        prompt += f"Topic: {tag}\n"
    if length:
        prompt += f"Desired length: {get_length_str(length)}\n"
    if language:
        prompt += f"Language: {language}\n"

    prompt += "\nReturn only the edited post text with no additional commentary."

    response = llm.invoke(prompt)
    return getattr(response, "content", response)


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))