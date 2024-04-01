import os
import json
import openai
import anthropic
import time

cfg = json.load(open('config.json', 'r'))

os.environ['OPENAI_API_KEY'] = cfg['openai_api_key']
openai_client = openai.OpenAI()

os.environ['ANTHROPIC_API_KEY'] = cfg['anthropic_api_key']
anthropic_client = anthropic.Anthropic()

def invoke(modelname, sysprompt, userprompt, assistantprompt=''):
    model_mapping = {
        "gpt3": "gpt-3.5-turbo-0125",
        "gpt4": "gpt-4-0125-preview",
        "haiku": "claude-3-haiku-20240307",
        "sonnet": "claude-3-sonnet-20240229",
        "opus": "claude-3-opus-20240229"
    }

    if modelname.startswith("gpt"):
        completion = openai_client.chat.completions.create(
            model=model_mapping[modelname],
            messages=[
                {"role": "system", "content": sysprompt},
                {"role": "user", "content": userprompt}])
        return completion.choices[0].message.content
    else:
        try:
            message = anthropic_client.messages.create(
                model=model_mapping[modelname],
                max_tokens=4096,
                system=sysprompt,
                messages=[
                    {"role": "user", "content": userprompt}])
            resp = message.content[0].text
            if resp.startswith('Here is'):
                resp = resp[resp.find('\n')+1:]
            return resp
        except anthropic.RateLimitError as e:
            print(f"Rate limited. Waiting 60 seconds...{e}")
            time.sleep(60) # anthropic is rate limited
            return invoke(modelname, sysprompt, userprompt)

    
# invoke the model N times and pick the one response that is most frequent
def invoke_N_times(modelname, sysprompt, userprompt, N):
    responses = []
    for i in range(N):
        response = invoke(modelname, sysprompt, userprompt)
        responses.append(response)
    return max(set(responses), key = responses.count)
