import glob,os,numpy as np,trimesh
from cert import coverage
D=os.environ.get("CADPROMPT_DIR","CADPrompt");PF="Natural_Language_Descriptions_Prompt_with_specific_measurements.txt"
ds=sorted(glob.glob(D+"/0*"));ms=[trimesh.load(d+"/Ground_Truth.stl") for d in ds];rng=np.random.default_rng(0)
c=[coverage(open(f"{d}/{PF}").read(),ms[(i+int(rng.integers(1,len(ds))))%len(ds)])[0] for i,d in enumerate(ds)]
c=np.array(c);print('NULL (other part) coverage mean',c.mean().round(3),'full',(c>=1).mean().round(3))
