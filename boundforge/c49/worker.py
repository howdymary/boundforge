import json,subprocess,time,pathlib
HERE=pathlib.Path(__file__).resolve().parent
def quantum(task,state,action,seed,ms=250,binary="/root/c49/search"):
 header=f"{task['kind']} {task['n']} {task['param']} {len(state)} {seed} {action} {ms}\n"
 start=time.monotonic();r=subprocess.run([binary],input=header+" ".join(map(str,state))+"\n",capture_output=True,text=True,timeout=ms/1000+15)
 if r.returncode:raise RuntimeError(r.stderr[:200])
 x=json.loads(r.stdout);x.update(wall_seconds=time.monotonic()-start,action=action,seed=seed)
 return x
def paired(task,state,seed,ms=250):
 probe=quantum(task,state,0,seed,ms)
 return {"probe":probe,"interventions":[quantum(task,probe["state"],a,seed+1000,ms) for a in range(6)]}
