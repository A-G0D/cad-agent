"""Pose-invariant CADPrompt score: min symmetric chamfer over the 24 proper axis rotations (prompts don't fix orientation; GT axes are arbitrary)."""
import os
import sys,json,glob,itertools,numpy as np,trimesh
from bench_cadprompt import norm,chamfer
R=[]
for p in itertools.permutations(range(3)):
  for s in itertools.product([1,-1],repeat=3):
    M=np.zeros((3,3))
    for i,j in enumerate(p): M[i,j]=s[i]
    if np.linalg.det(M)>0: R.append(M)
if __name__=="__main__":
  d=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'results/cadprompt_merged.json'));out={}
  for r in d:
    f=f"/tmp/cadp_{r['id']}.stl"
    if r.get('cd') is None or r['cd']>=5: out[r['id']]=5.196;continue
    G=norm(trimesh.load(f"{os.environ.get("CADPROMPT_DIR","CADPrompt")}/{r['id']}/Ground_Truth.stl"));P=norm(trimesh.load(f))
    out[r['id']]=min(chamfer(G,P@M.T) for M in R)
  v=np.array(list(out.values()));json.dump(out,open(sys.argv[2] if len(sys.argv)>2 else 'results/cadprompt_poseinv.json','w'))
  print('median',np.median(v).round(4),'<0.05',(v<.05).mean(),'<0.02',(v<.02).mean())
