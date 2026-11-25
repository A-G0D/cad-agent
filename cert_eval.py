import json,numpy as np
d=json.load(open('results/cert_score.json'));cd=np.array([v['cd'] for v in d.values()]);cov=np.array([v['cov'] for v in d.values()]);ok=np.array([v['ok'] for v in d.values()])
y=cd<.05;print('n',len(d),'correct(poseinv<.05)',y.mean().round(3),'gate ok',ok.mean().round(3),'acc|ok',y[ok].mean().round(3),'acc|!ok',y[~ok].mean().round(3))
pos,neg=cov[y],cov[~y];print('AUC cov',np.mean([(p>n)+.5*(p==n) for p in pos for n in neg]).round(3))
for t in (1.0,.8,.5):
  s=cov>=t;print('cov>=',t,'n',s.sum(),'acc',y[s].mean().round(3),'| below: n',(~s).sum(),'acc',y[~s].mean().round(3) if (~s).any() else None)
s=(cov>=1)&ok;print('cov1&ok n',s.sum(),'acc',y[s].mean().round(3))
for i,v in list(d.items()):
  if v['cd']>=.05 and v['cov']>=1: print('FALSE-CERT',i,round(v['cd'],3))

from scipy.stats import spearmanr
print('spearman(cov,cd)',spearmanr(cov,cd))
