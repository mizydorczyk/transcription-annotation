import pandas as pd

class Argument:
    def __init__(self, conclusion_id, conclusion_sentence, conclusion_details, premises):
        self.conclusion_id = conclusion_id
        self.conclusion_sentence = conclusion_sentence
        self.conclusion_details = conclusion_details
        self.premises = premises

    def __repr__(self):
        return (f"Conclusion ID: {self.conclusion_id}\n"
                f"Conclusion Sentence: {self.conclusion_sentence}\n"
                f"Conclusions: {self.conclusion_details}\n"
                f"Premises: {self.premises}")


def parse_annotations(filepath):
    annotations = pd.read_csv(filepath)

    grouped = annotations.groupby(['conclusion_id', 'conclusion_sentence'])
    arguments = []

    for (conclusion_id, conclusion_sentence), group in grouped:
        conclusion_details = {}
        premises = []

        for _, row in group.iterrows():
            annotator = row['annotator']
            conclusion = row['conclusion']
            conclusion_details[annotator] = conclusion

            for i in range(1, 9):
                premise_id = row.get(f'premise_{i}_id')
                premise_sentence = row.get(f'premise_{i}_sentence')

                if pd.notna(premise_id) and pd.notna(premise_sentence):
                    premises.append({
                        'annotator': annotator,
                        'premise_id': premise_id,
                        'premise_sentence': premise_sentence
                    })

        arguments.append(Argument(conclusion_id, conclusion_sentence, conclusion_details, premises))

    return arguments


def generate_html(arguments, output_file):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arguments</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        .conclusion {
            font-weight: bold;
            color: #333;
        }
        .premise {
            color: #555;
        }
        .annotator {
            font-style: italic;
            color: #007BFF;
        }
    </style>
</head>
<body>
    <h1>Summary</h1>
"""

    for argument in arguments:
        html += f"""
        <table>
            <tr>
                <th colspan="2">Conclusion ID: {argument.conclusion_id}</th>
            </tr>
            <tr>
                <td colspan="2" class="conclusion">{argument.conclusion_sentence}</td>
            </tr>
            <tr>
                <th>Annotator</th>
                <th>Conclusion</th>
            </tr>
        """

        for annotator, conclusion in argument.conclusion_details.items():
            html += f"""
            <tr>
                <td class="annotator">{annotator}</td>
                <td>{conclusion}</td>
            </tr>
            """

        if argument.premises:
            html += """
            <tr>
                <th colspan="2">Premises</th>
            </tr>
            <tr>
                <th>Annotator</th>
                <th>Premise Details</th>
            </tr>
            """
            for premise in argument.premises:
                html += f"""
                <tr>
                    <td class="annotator">{premise['annotator']}</td>
                    <td class="premise">ID: {premise['premise_id']}<br>{premise['premise_sentence']}</td>
                </tr>
                """
        html += "</table>"

    html += """
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    filepath = 'assets/annotations.csv'
    output_file = 'assets/summary.html'

    arguments = parse_annotations(filepath)

    generate_html(arguments, output_file)


if __name__ == '__main__':
    main()
