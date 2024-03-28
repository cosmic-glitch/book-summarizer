import os
import json
import openai
import anthropic

cfg = json.load(open('config.json', 'r'))

os.environ['OPENAI_API_KEY'] = cfg['openai_api_key']
openai_client = openai.OpenAI()

os.environ['ANTHROPIC_API_KEY'] = cfg['anthropic_api_key']
anthropic_client = anthropic.Anthropic()

def invoke_llm(modelname, sysprompt, userprompt):
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
        message = anthropic_client.messages.create(
            model=model_mapping[modelname],
            max_tokens=4096,
            messages=[{"role": "user", "content": sysprompt + '\nFull Text:\n' + userprompt}])
        return message.content
