import openai
import anthropic
import time
import dotenv
import ollama

dotenv.load_dotenv()
openai_client = openai.OpenAI()
anthropic_client = anthropic.Anthropic()
anthropic_gcp_client = anthropic.AnthropicVertex(region="us-central1", project_id="fresh-runway-421006")

def invoke(modelname, sysprompt, userprompt, assistantprompt=''):
    model_mapping = {
        "gpt3": "gpt-3.5-turbo-0125",
        "gpt4": "gpt-4-turbo-2024-04-09",
        "haiku": "claude-3-haiku-20240307",
        "haiku@gcp": "claude-3-haiku@20240307",
        "sonnet": "claude-3-sonnet-20240229",
        "opus": "claude-3-opus-20240229"
    }

    if modelname.startswith("gpt"):
        try:
            completion = openai_client.chat.completions.create(
                model=model_mapping[modelname],
                messages=[
                    {"role": "system", "content": sysprompt},
                    {"role": "user", "content": userprompt}])
            return completion.choices[0].message.content
        except openai.BadRequestError as e:
            print(f"Bad request. {e}")
            return invoke("haiku", sysprompt, userprompt)
        
    elif modelname.startswith("llama3"):
        prompt = f"{sysprompt}\nHere's the text:\n{userprompt}"
        response = ollama.generate('llama3:8b', prompt)
        return response['response']

    else:
        client = anthropic_gcp_client if modelname.endswith("@gcp") else anthropic_client
        try:
            message = client.messages.create(
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
