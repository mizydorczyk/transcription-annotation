import pandas as pd
from sklearn.metrics import cohen_kappa_score

def main():
    annotations = pd.read_csv('assets/canonical-vs-noncanonical-annotator-1-vs-2.csv', index_col = 0)
    annotations = annotations.apply(pd.to_numeric, errors='coerce')

    condition_a_annotations = annotations[['anotator_1_a', 'anotator_2_a']].dropna()
    condition_b_annotations = annotations[['anotator_1_b', 'anotator_2_b']].dropna()
    condition_c_annotations = annotations[['anotator_1_c', 'anotator_2_c']].dropna()
    condition_d_annotations = annotations[['anotator_1_d', 'anotator_2_d']].dropna()

    print('{value:.3f}'.format(value = cohen_kappa_score(condition_a_annotations[['anotator_1_a']], condition_a_annotations[['anotator_2_a']])))
    print('{value:.3f}'.format(value = cohen_kappa_score(condition_b_annotations[['anotator_1_b']], condition_b_annotations[['anotator_2_b']])))
    print('{value:.3f}'.format(value = cohen_kappa_score(condition_c_annotations[['anotator_1_c']], condition_c_annotations[['anotator_2_c']])))
    print('{value:.3f}'.format(value = cohen_kappa_score(condition_d_annotations[['anotator_1_d']], condition_d_annotations[['anotator_2_d']])))

if __name__ == '__main__':
    main()

'''
0.475
0.548
0.661
0.808
'''