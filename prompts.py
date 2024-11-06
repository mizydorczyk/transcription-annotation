import pandas as pd
import json

transcript = pd.read_csv('assets/transcript.csv', index_col = 1)
questions_ids = transcript.index[transcript.is_question == 1]
context_depth = 3

base_prompt = '''Jesteś anotatorem zbioru językowego. Dokonaj analizy zdania pod kątem spełniania następujących warunków. Zdania przed i po służą jako kontekst.
Warunek A: Mówiący jest neutralny względem możliwych rozwiązań kwestii, którą porusza.
Warunek B: Mówiący może zakładać, że adresat zna informację, która rozstrzyga poruszaną przez niego kwestię.
Warunek C: Mówiący może zakładać, że adresat udzieli tej informacji w najbliższej przyszłości rozmowy w wyniku aktu mowy mówiącego.
Warunek D: Głównym celem, jaki realizuje mówiący, poruszając kwestię, jest jej rozwiązanie w najbliższej przyszłości.
'''

prompts = []

for question_id in questions_ids:
    try:
        instruction = f'Oceń, czy zdanie {question_id} spełnia powyższe warunki, biorąc pod uwagę poniższy kontekst:\n'

        data = 'id zdania | id mówiącego | zdanie\n'
        for counter in range(2 * context_depth + 1):
            index = question_id - context_depth + counter
            if index in transcript.index:
                data += f'{index} | {transcript.speaker_id[index]} | {transcript.sentence[index]}\n'

        prompts.append(base_prompt + instruction + data)
    except Exception as e:
        print(e)

with open(f'assets/prompts_ctx_depth_{context_depth}.json', 'w', encoding = 'utf-8') as json_file:
    json.dump(prompts, json_file, ensure_ascii=False, indent = 4)