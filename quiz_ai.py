import json
import sys
import yaml
from google_gemini_api import send_query_to_ai

def gen_prompt(topic, n) :

    prompt_input = '''
    # {} Expertise Quiz for the topic "{}"\n 
    ### 4 options required along with a correct answer \n
    ### Use the YAML Format as shown below ###\n
    ---
    1: 
      question: ""
      options:
        a: ""
        b: ""
        c: ""
        d: ""
      answer: single character either a/b/c/d
    2: 
    and so on.."" \n
    ### Prefer text instead of special characters
    ### do not include the char ```
    '''.format(n, topic)

    return prompt_input

def get_quiz_dict(topic, count):
    prompt_input = gen_prompt(topic, count)
    while True:
        resp = send_query_to_ai(prompt_input)

        if not resp:
            sys.exit()

        try:
            quiz_dict = yaml.safe_load(resp)
            return quiz_dict
        except Exception as e:
            print(e)
            print("Retrying.. ")

if __name__ == '__main__':
    pass
