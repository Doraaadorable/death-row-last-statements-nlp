"""Protocol-based follow-up; published data and result directories stay unchanged."""
import hashlib
import json
import platform
import warnings
from itertools import combinations
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
import sklearn
from scipy.optimize import linear_sum_assignment
from sklearn.decomposition import NMF
from sklearn.exceptions import ConvergenceWarning
from text_features import make_vectorizer, identical_column_groups, group_jaccard, verify_reference

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/followup_audit_v1'
OUT.mkdir(exist_ok=True)
BASE = ROOT / 'results/nmf_v2'
source = ROOT / 'data/processed/model_corpus_v1.csv'
manifest = json.loads((BASE / 'run_manifest.json').read_text())
if hashlib.sha256(source.read_bytes()).hexdigest() != manifest['source_sha256']:
    raise ValueError('Source hash differs from published run')
df = pd.read_csv(source, keep_default_na=False)
df = df.loc[df.preparation_status.eq('ready_for_exploration')].sort_values('execution_number')
vectorizer = make_vectorizer(manifest['vectorizer_parameters'])
X = vectorizer.fit_transform(df.model_text)
keep = np.asarray(X.getnnz(axis=1)).ravel() > 0
df = df.loc[keep].reset_index(drop=True)
X = X[keep]
terms = vectorizer.get_feature_names_out()
if X.shape != (manifest['documents_modeled'], manifest['features']):
    raise ValueError('Feature matrix dimensions differ')
groups = identical_column_groups(X)
pd.DataFrame([{'group_id': i, 'term': str(terms[j]), 'size': len(g)}
              for i,g in enumerate(groups) for j in g]).to_csv(OUT/'feature_groups.csv',index=False)
runs, pairs, references = [], [], []
for k in [4,6,8]:
    fitted = {}
    for name, init, seed in [('reference','nndsvda',42)] + [(str(s),'random',s) for s in range(5)]:
        model = NMF(n_components=k, init=init, random_state=seed, max_iter=1000, tol=1e-4)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always', ConvergenceWarning)
            model.fit(X)
        H = model.components_
        H = H / np.linalg.norm(H, axis=1, keepdims=True)
        fitted[name] = H
        runs.append({'k':k,'run':name,'converged':not any(issubclass(w.category,ConvergenceWarning) for w in caught),
                     'iterations':model.n_iter_,'reconstruction_error':model.reconstruction_err_,
                     'captured_squared_norm_fraction':1-model.reconstruction_err_**2/float(X.multiply(X).sum())})
    verify_reference(BASE,k,fitted['reference'],terms,X)
    for a,b in list(combinations([str(s) for s in range(5)],2)) + [('reference',str(s)) for s in range(5)]:
        sim = fitted[a] @ fitted[b].T
        left,right = linear_sum_assignment(-sim)
        for i,j in zip(left,right):
            row={'k':k,'left_run':a,'right_run':b,'left_topic':int(i+1),'right_topic':int(j+1),
                 'cosine_similarity':float(sim[i,j]),'top15_group_jaccard':group_jaccard(fitted[a][i],fitted[b][j],terms,groups)}
            (references if a=='reference' else pairs).append(row)
pairs = pd.DataFrame(pairs)
pairs.to_csv(OUT/'random_pairwise_topics.csv',index=False)
pd.DataFrame(references).to_csv(OUT/'reference_vs_random_topics.csv',index=False)
pd.DataFrame(runs).to_csv(OUT/'runs.csv',index=False)
summary = pairs.groupby('k').cosine_similarity.agg(minimum='min',lower_quartile=lambda x:x.quantile(.25),median='median')
summary.to_csv(OUT/'random_pairwise_summary.csv')
labels = pd.read_csv(ROOT/'data/processed/annotation_development_v2.csv',keep_default_na=False)
if not labels.execution_number.is_unique or len(labels)!=50:
    raise ValueError('Unexpected annotation sample')
weights = pd.read_csv(BASE/'document_weights_k6.csv')
joined = labels.merge(weights,on='execution_number',validate='one_to_one',how='left',indicator=True)
if not joined['_merge'].eq('both').all():
    raise ValueError('Missing annotated document weights')
mappings={1:['apology_forgiveness','harm_acknowledgment'],2:['relational_affection'],3:['innocence_dispute'],4:['faith_spirituality'],5:['gratitude','farewell_readiness']}
contrasts=[]
for topic, names in mappings.items():
    for label in names:
        if not joined[label].astype(str).isin(['0','1','u']).all():
            raise ValueError('Unexpected frozen label value')
        for value in ['0','1','u']:
            values=joined.loc[joined[label].astype(str).eq(value),f'topic_{topic}']
            contrasts.append({'topic':topic,'label':label,'value':value,'n':len(values),
                              'q1':values.quantile(.25),'median':values.median(),'q3':values.quantile(.75)})
pd.DataFrame(contrasts).to_csv(OUT/'topic_label_descriptive.csv',index=False)
metadata={'scope':'Follow-up on fixed v2 feature space; no independent validation',
          'source_sha256':manifest['source_sha256'],'annotation_sha256':hashlib.sha256((ROOT/'data/processed/annotation_development_v2.csv').read_bytes()).hexdigest(),
          'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__,
          'features':X.shape[1],'groups':len(groups),'duplicate_groups':sum(len(g)>1 for g in groups),'features_in_duplicate_groups':sum(len(g) for g in groups if len(g)>1),
          'protocol_commit':'2b4157c1a01d7c99e419d1059af1eb487b9090bf',
          'reference_provenance':'Regenerated after protocol; validated against historical partial term weights and full document coefficients. Historical full H was not available.'}
(OUT/'manifest.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(summary.round(6).to_string())
print('Saved:',OUT)
