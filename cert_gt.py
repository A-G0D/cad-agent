import glob,os,json,numpy as np,trimesh
from cert import coverage
D=os.environ.get("CADPROMPT_DIR","CADPrompt");PF="Natural_Language_Descriptions_Prompt_with_specific_measurements.txt"
cs=[];ms=[]
for dd in sorted(glob.glob(D+"/0*")):
    c,m=coverage(open(f"{dd}/{PF}").read(),trimesh.load(dd+"/Ground_Truth.stl"));cs.append(c);ms.append((os.path.basename(dd),m))
cs=np.array(cs);print('GT self-coverage mean',cs.mean().round(3),'full',(cs>=1).mean().round(3),'n',len(cs))
bad=[x for x,c in zip(ms,cs) if c<1][:6];print(bad)
json.dump(dict(zip([x[0] for x in ms],cs.tolist())),open('results/gt_cov.json','w'))
