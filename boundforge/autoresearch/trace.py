"""Hash-chained decisions and atomic resume state; exact hashes, not model prose."""
import datetime as dt,hashlib,json,os,pathlib
def canonical(v):return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=True)
def digest(v):return hashlib.sha256(canonical(v).encode()).hexdigest()
class Trace:
 def __init__(self,out):
  self.out=pathlib.Path(out);self.out.mkdir(parents=True,exist_ok=True);self.path=self.out/"decisions.jsonl";self.events=[]
  if self.path.exists():
   previous="0"*64
   for line in self.path.read_text().splitlines():
    e=json.loads(line);h=e.pop("hash")
    if e["previous"]!=previous or digest(e)!=h or e["seq"]!=len(self.events):raise ValueError("trace chain invalid")
    e["hash"]=h;self.events.append(e);previous=h
 def add(self,kind,**data):
  e={"seq":len(self.events),"utc":dt.datetime.now(dt.timezone.utc).isoformat(),"kind":kind,"previous":self.events[-1]["hash"]if self.events else "0"*64,"data":data};e["hash"]=digest(e)
  with self.path.open("a")as p:p.write(canonical(e)+"\n");p.flush();os.fsync(p.fileno())
  self.events.append(e);return e["hash"]
 def save(self,state):
  state["trace_head"]=self.events[-1]["hash"] if self.events else "0"*64
  state.pop("state_sha256",None);state["state_sha256"]=digest(state)
  p=self.out/"checkpoint.tmp";p.write_text(canonical(state)+"\n");os.replace(p,self.out/"checkpoint.json")
def validate_trace(path):return Trace(pathlib.Path(path).parent).events
