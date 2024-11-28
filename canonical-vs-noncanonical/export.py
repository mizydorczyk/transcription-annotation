import json
import pandas as pd

def main():
    with open('canonical-vs-noncanonical\runs\run1\prompts_and_responses_ctx_depth_3.json', 'r', encoding = 'utf8') as file:
      responses = json.load(file)
      rows = []
        
      for response in responses:
        response_dict = json.loads(response["response"])
        row = {
            "question_id": response["question_id"],
            "warunek_a": response_dict["warunek_a"],
            "warunek_b": response_dict["warunek_b"],
            "warunek_c": response_dict["warunek_c"],
            "warunek_d": response_dict["warunek_d"]
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv('canonical-vs-noncanonical\runs\run1\prompts_and_responses_ctx_depth_3.csv', index=False)

if __name__ == '__main__':
    main()