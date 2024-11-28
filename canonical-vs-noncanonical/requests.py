import json
import logging
from openai import OpenAI

def send_prompt(client, prompt):
  return client.chat.completions.create(
  model = 'gpt-4o-mini',
  messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ],
  temperature = 0.7,
  max_tokens = 64,
  top_p = 0.8,
  frequency_penalty = 0,
  presence_penalty = 0,
  response_format = {
    'type': 'json_schema',
    'json_schema': {
      'name': 'binary_conditions_model',
      'schema': {
        'type': 'object',
        'required': [
          'warunek_a',
          'warunek_b',
          'warunek_c',
          'warunek_d'
        ],
        'properties': {
          'warunek_a': {
            'type': 'number',
            'description': 'Wskazuje, czy warunek A jest spełniony. Wartość `1` oznacza, że warunek zachodzi, podczas gdy `0` oznacza, że warunek nie zachodzi.'
          },
          'warunek_b': {
            'type': 'number',
            'description': 'Wskazuje, czy warunek B jest spełniony. Wartość `1` oznacza, że warunek zachodzi, podczas gdy `0` oznacza, że warunek nie zachodzi.'
          },
          'warunek_c': {
            'type': 'number',
            'description': 'Wskazuje, czy warunek C jest spełniony. Wartość `1` oznacza, że warunek zachodzi, podczas gdy `0` oznacza, że warunek nie zachodzi.'
          },
          'warunek_d': {
            'type': 'number',
            'description': 'Wskazuje, czy warunek D jest spełniony. Wartość `1` oznacza, że warunek zachodzi, podczas gdy `0` oznacza, że warunek nie zachodzi.'
          }
        },
        'additionalProperties': False
      },
      'strict': True
    }
  }
  )

logger = logging.getLogger(__name__)
   
def main():
  logging.basicConfig(filename='canonical-vs-noncanonical/runs/run1/requests.log', level=logging.INFO, encoding='utf8')
  logger.info('started')

  with open('canonical-vs-noncanonical/runs/run1/prompts_ctx_depth_3.json', 'r', encoding = 'utf8') as file:
      prompts = json.load(file)

  client = OpenAI()

  responses = []

  for prompt in prompts:
    logger.info(f'Prompt:\n{prompt['prompt']}')
    try:
      response = send_prompt(client, prompt['prompt'])
      content = response.choices[0].message.content

      responses.append({
        'question_id': prompt['question_id'],
        'prompt': prompt['prompt'],
        'response': content
      })

      logger.info(f'Response:\n{content}')
    except Exception as e:
      logger.error(e)
  
  with open('runs/run1/prompts_and_responses_ctx_depth_3.json', 'w', encoding='utf8') as json_file:
    json.dump(responses, json_file, indent=4, ensure_ascii=False)


  logger.info('completed')

if __name__ == '__main__':
  main()

'''
Jesteś anotatorem zbioru językowego. Dokonaj analizy zdania pod kątem spełniania następujących warunków. Zdania przed i po służą jako kontekst.
Warunek A: Mówiący jest neutralny względem możliwych rozwiązań kwestii, którą porusza.
Warunek B: Mówiący może zakładać, że adresat zna informację, która rozstrzyga poruszaną przez niego kwestię.
Warunek C: Mówiący może zakładać, że adresat udzieli tej informacji w najbliższej przyszłości rozmowy w wyniku aktu mowy mówiącego.
Warunek D: Głównym celem, jaki realizuje mówiący, poruszając kwestię, jest jej rozwiązanie w najbliższej przyszłości.
Oceń, czy zdanie 37 spełnia powyższe warunki, biorąc pod uwagę poniższy kontekst:
id zdania | id mówiącego | zdanie
34 | 1 | Może zacznijmy od pań ekspertek.
35 | 1 | Pani profesor Ewa Dmoch-Gajzlerska.
36 | 2 | Dobrze, odpowiadam krótko: nie.
37 | 1 | A dlaczego?
38 | 2 | Dlatego, że ja, mając czterdzieści sześć lat pracy, już przeżyłam szereg sytuacji związanych z aborcją.
39 | 2 | Ja również — nie, absolutnie nie wypieram się, że wykonywałam zabiegi przerwania ciąży, bo to w tamtych czasach to było konieczne, ale równocześnie rozwój technik wizualizacji innych, które sprawiły, że zobaczyliśmy, jak rozwija się dziecko czy płód w macicy, wszystko to sprawiło, że ja zablokowałam się i absolutnie, muszę powiedzieć, że od pewnego momentu nie wykonywałam zabiegów i równocześnie te zabiegi były oczywiście robione w tych szpitalach, w których ja pracowałam, ale ja w nich nie uczestniczyłam.
40 | 1 | Pani doktor Orawiec — czy pani jest za legalizacją aborcji, do dwunastego tygodnia ciąży, rzecz jasna?

ChatCompletion(id='chatcmpl-AQhPuRFFHK2sU0FlL4iR7KLkhxHDZ', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='{"warunek_a":1,"warunek_b":1,"warunek_c":1,"warunek_d":1}', refusal=None, role='assistant', audio=None, function_call=None, tool_calls=None))], created=1730926786, model='gpt-4o-mini-2024-07-18', object='chat.completion', service_tier=None, system_fingerprint='fp_0ba0d124f1', usage=CompletionUsage(completion_tokens=25, prompt_tokens=826, total_tokens=851, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))

{
  "warunek_a": 1,
  "warunek_b": 1,
  "warunek_c": 1,
  "warunek_d": 1
}
'''