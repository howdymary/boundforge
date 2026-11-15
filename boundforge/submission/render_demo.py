"""Build an offline trace viewer and a120s captioned video from REAL frozen artifacts."""
import hashlib,html,json,pathlib,subprocess,textwrap
from fractions import Fraction as F
from PIL import Image,ImageDraw,ImageFont
HERE=pathlib.Path(__file__).resolve().parent;BASE=HERE.parent/"autoresearch/results/2026-11-15";OUT=HERE/"demo"
def decimal(q,places=18,up=False):
 q=F(q);scale=10**places;n=-((-q.numerator*scale)//q.denominator)if up else q.numerator*scale//q.denominator
 return str(n//scale)+"."+str(n%scale).zfill(places)
HTML=r"""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BoundForge — inspect the research loop</title>
<style>
:root{--ink:#142728;--paper:#f4f4ec;--muted:#596866;--green:#147a58;--orange:#b65f18;--line:#ced8cf;--card:#fffef8}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:38px 32px 70px}header{display:flex;justify-content:space-between;align-items:start;gap:30px;border-bottom:1px solid var(--line);padding-bottom:24px}.eyebrow{font:12px ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--green)}h1{font-size:54px;line-height:1.05;margin:10px 0 12px;letter-spacing:-.055em}h2{font-size:22px;letter-spacing:-.03em;margin:0 0 14px}p{margin:7px 0}.subtitle{max-width:650px;color:var(--muted)}.pill{border:1px solid var(--line);padding:7px 12px;border-radius:30px;font-size:12px;white-space:nowrap}.hero{display:grid;grid-template-columns:2fr 1fr;gap:22px;margin:24px 0}.card{background:var(--card);border:1px solid var(--line);border-radius:15px;padding:24px}.bound{font:clamp(18px,3vw,34px) ui-monospace,monospace;letter-spacing:-.045em;color:var(--green);margin:15px 0;overflow-wrap:anywhere}.small{font-size:12px;color:var(--muted)}.grid{display:grid;grid-template-columns:1.25fr 1fr;gap:22px}.flow{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 24px}.node{font-size:12px;border:1px solid var(--line);border-radius:7px;padding:7px 10px}.node.active{background:var(--ink);color:white;border-color:var(--ink)}.controls{display:flex;align-items:center;gap:10px;margin:18px 0}button{font:inherit;color:var(--ink);background:var(--paper);border:1px solid var(--line);border-radius:7px;padding:7px 14px;cursor:pointer}button:hover{border-color:var(--green)}button:focus-visible,input:focus-visible{outline:3px solid var(--orange)}input{flex:1;min-width:70px;accent-color:var(--green)}.event{min-height:175px;border-left:3px solid var(--orange);padding-left:16px}.event h3{margin:0 0 10px;font-size:20px}.hash{font:11px ui-monospace,monospace;overflow-wrap:anywhere;color:var(--muted)}pre{font:12px/1.5 ui-monospace,monospace;max-height:320px;overflow:auto;white-space:pre-wrap;word-break:break-word;background:#edf0e8;padding:14px;border-radius:8px}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:9px 5px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}.ok{color:var(--green);font-weight:650}.warn{color:var(--orange)}.sources a{color:var(--green);overflow-wrap:anywhere}.sources li{margin-bottom:8px}details{margin-top:14px}summary{cursor:pointer;font-size:13px}.limits{margin-top:22px;background:#e8ede4}.limits strong{color:var(--orange)}footer{margin-top:25px;font-size:12px;color:var(--muted)}a{color:var(--green)}@media(max-width:850px){main{padding:20px}.hero,.grid{grid-template-columns:1fr}h1{font-size:44px}header{display:block}.pill{display:inline-block;margin-top:15px}}
</style><main>
<header><div><div class="eyebrow">Track1 / C51a / actual-artifact replay</div><h1>BoundForge</h1><p class="subtitle">Choose an experiment. Measure what happened. Verify the mathematics before accepting the result.</p></div><div class="pill">Historical replay, not a blind discovery</div></header>
<section class="hero"><div class="card"><div class="eyebrow">Certified lower bound</div><div class="bound" id="bound"></div><p id="margin"></p><p class="small">A very small conventional parameter refinement in the established He–Tang family. Full-circle and infinite-tail certificates included.</p></div><div class="card"><div class="eyebrow">This recorded execution</div><h2 id="runtime"></h2><p id="steps"></p><p class="small">The playback below is slowed for inspection. It does not trigger APIs or run new experiments.</p></div></section>
<section class="grid"><div class="card"><h2>Follow the next decision</h2><div class="flow" id="flow"></div><div class="event" aria-live="polite"><div class="eyebrow" id="kind"></div><h3 id="eventtitle"></h3><p id="explanation"></p><p class="hash" id="hash"></p></div><div class="controls"><button id="back" aria-label="Previous event">←</button><button id="play">Play</button><input id="range" type="range" min="0" aria-label="Research event"><button id="next" aria-label="Next event">→</button></div><div class="small" id="position"></div><details><summary>Inspect the actual event JSON</summary><pre id="raw"></pre></details></div>
<div class="card"><h2>One result, three checkers</h2><table><thead><tr><th>Implementation</th><th>Complete cover</th><th>Nodes</th></tr></thead><tbody id="checkers"></tbody></table><p class="small">Two independently implemented algorithms share mpmath; the separately authored published verifier uses decimal intervals. Execution is not independent human endorsement.</p><details><summary>Exact comparison and witness</summary><pre id="witness"></pre></details></div></section>
<section class="grid" style="margin-top:22px"><div class="card"><h2>Strong controls, honest outcome</h2><p class="small">Three paired seeds, one incumbent. Same maximum allowances. Goal: exceed the pre-existing project bound.</p><table><thead><tr><th>Policy</th><th>Goal /3</th><th>Median loop s</th></tr></thead><tbody id="comparison"></tbody></table><p class="warn">Fixed high precision is faster. No controller-advantage claim.</p><p class="small">Float also verifies smaller external-reference improvements; those are retained as progress rather than called mathematical failures.</p></div>
<div class="card sources"><h2>Sources used inside the loop</h2><ul id="sources"></ul><p class="small" id="sourcegate"></p><details><summary>Model action — unverified rationale</summary><pre id="model"></pre></details></div></section>
<section class="card limits"><h2>What this establishes</h2><p>A runnable bounded loop, genuine action changes, exact witnesses and a tiny certified bound improvement over the audited external construction.</p><p><strong>What it does not establish:</strong> a new general algorithm, a memory/model advantage, broad generalization, external peer review or a blind standalone discovery. The portable runner was built after the initial agent-directed research.</p></section>
<footer><p><a href="https://github.com/howdymary/boundforge">Repository</a> · <a href="https://github.com/howdymary/boundforge/blob/main/boundforge/submission/SUBMISSION.md">Submission draft</a> · <a href="https://github.com/howdymary/boundforge/blob/main/boundforge/submission/MATH_VERIFICATION.md">Mathematics and trust boundary</a> · <button id="download">Download actual replay data</button></p><p id="provenance"></p></footer>
</main><script>
"use strict";
const DATA=__DATA__;
const $=s=>document.querySelector(s);
const stages=["Source","Choose","Run","Diagnose","Verify","Retain"];
stages.forEach(s=>{const e=document.createElement("span");e.className="node";e.textContent=s;$("#flow").appendChild(e)});
$("#bound").textContent="C51a > "+DATA.pretty_bound;
$("#margin").textContent="More than 1.58 × 10⁻¹⁷ above an upper bound on the actual strongest external prior function found.";
$("#runtime").textContent=DATA.report.elapsed_seconds.toFixed(2)+" seconds";
$("#steps").textContent=DATA.report.experiments.length+" experiments; all decisions recorded.";
const events=DATA.events;let index=0,timer=null;
const labels={campaign_start:"Begin a source-pinned challenge",baseline_certified:"Reproduce the exact incumbent",decision:"Choose the next experiment",experiment_started:"Launch the isolated worker",experiment_result:"Read measured evidence",certification_requested:"Ask protected checkers",valid_improvement_below_continuation_goal:"Valid progress, below the current goal",exa_frontier_gate:"Confirm the full witness through Exa",tinker_operator_proposal:"Receive a bounded model suggestion",tinker_unavailable:"Retain failure and use the disclosed fallback",certified_improvement:"Accept only after proof checks",campaign_finished:"Stop and preserve the result",provider_reservation:"Reserve credits before a call"};
function explain(e){const d=e.data;
if(e.kind==="decision")return "Action: "+d.action+". "+d.why.reason+". Retrieved record IDs: "+(d.why.retrieved||[]).map(x=>x.slice(0,12)).join(", ");
if(e.kind==="experiment_result")return d.diagnosis+"; evidence: "+JSON.stringify(d.evidence);
if(e.kind==="valid_improvement_below_continuation_goal")return "The float proposal is mathematically valid, but does not exceed the existing project bound. The loop retains it and continues.";
if(e.kind==="exa_frontier_gate")return d.registered_witness_confirmed?"Search plus full contents confirmed the exact prior parameter pair. This gate permitted further search.":"Source confirmation failed; the run cannot claim this frontier.";
if(e.kind==="tinker_operator_proposal")return "Proposed operator: "+d.result.action+". The explanation is not treated as a proof.";
if(e.kind==="certified_improvement")return "Both own full-domain checkers and the separately authored checker passed. The new bound exceeds the registered external function and the existing project claim.";
if(e.kind==="campaign_finished")return "Status: "+d.status+". Fresh blind world-record discovery claimed: false.";
if(e.kind==="baseline_certified")return "Checker: "+d.checker+". Whole-circle certificate reproduced before research begins.";
if(e.kind==="experiment_started")return "Operator: "+d.operator+". The proposal container has no repository, saved answer, network or credentials.";
if(e.kind==="certification_requested")return "Numerical output is only a proposal. Independent acceptance runs outside the search worker.";
return "Actual recorded event; inspect its JSON and source hashes below.";}
function phase(k){if(k.includes("exa")||k==="campaign_start")return0;if(k==="decision"||k.includes("tinker"))return1;if(k==="experiment_started")return2;if(k==="experiment_result"||k.includes("below_"))return3;if(k.includes("certif")||k==="baseline_certified")return4;return5;}
function show(){const e=events[index];$("#kind").textContent=e.kind;$("#eventtitle").textContent=labels[e.kind]||e.kind;$("#explanation").textContent=explain(e);$("#hash").textContent="Event "+e.hash;$("#raw").textContent=JSON.stringify(e,null,2);$("#position").textContent=(index+1)+" / "+events.length+" recorded events";$("#range").value=index;document.querySelectorAll(".node").forEach((n,i)=>n.classList.toggle("active",i===phase(e.kind)));}
$("#range").max=events.length-1;$("#range").addEventListener("input",e=>{index=Number(e.target.value);show()});$("#back").onclick=()=>{index=Math.max(0,index-1);show()};$("#next").onclick=()=>{index=Math.min(events.length-1,index+1);show()};
$("#play").onclick=()=>{if(timer){clearInterval(timer);timer=null;$("#play").textContent="Play";return}$("#play").textContent="Pause";timer=setInterval(()=>{index=(index+1)%events.length;show()},1500)};
for(const row of DATA.checker_rows){const tr=document.createElement("tr");for(const v of [row.name,"PASS",row.nodes]){const td=document.createElement("td");td.textContent=v;if(v==="PASS")td.className="ok";tr.appendChild(td)}$("#checkers").appendChild(tr)}
for(const [key,v]of Object.entries(DATA.controls.medians)){const tr=document.createElement("tr");for(const x of[key.replaceAll("_"," "),v.successes+" / 3",v.loop_wall_seconds.toFixed(2)]){const td=document.createElement("td");td.textContent=x;tr.appendChild(td)}$("#comparison").appendChild(tr)}
const seen=new Set();for(const e of DATA.source_entries){if(!/^https?:\/\//.test(e.url||"")||seen.has(e.url))continue;seen.add(e.url);const li=document.createElement("li"),a=document.createElement("a");a.href=e.url;a.textContent=e.title||e.url;a.rel="noopener";li.appendChild(a);$("#sources").appendChild(li)}
$("#sourcegate").textContent="Full parameter pair confirmed: "+DATA.source_confirmed+". API request IDs: "+DATA.request_ids.join(", ");
$("#model").textContent=JSON.stringify(DATA.model_event||{status:"No successful model event in this run."},null,2);
$("#witness").textContent=JSON.stringify({candidate:DATA.candidate,previous_actual_beta_upper_decimal:DATA.previous_upper,certificate_sha256:DATA.report.accepted.candidate_sha256},null,2);
$("#provenance").textContent="Frozen source "+DATA.report.source_sha+" · run "+DATA.report.run_id+" · no new experiment is launched by this viewer.";
$("#download").onclick=()=>{const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([JSON.stringify(DATA,null,2)],{type:"application/json"}));a.download="boundforge-actual-replay.json";a.click();URL.revokeObjectURL(a.href)};
show();
</script></html>""".replace("return0","return 0").replace("return1","return 1").replace("return2","return 2").replace("return3","return 3").replace("return4","return 4").replace("return5","return 5")
def load():
 chosen=BASE/"providers-model";report=json.loads((chosen/"report.json").read_text());candidate=json.loads((chosen/"candidate.json").read_text());events=[json.loads(l)for l in(chosen/"decisions.jsonl").read_text().splitlines()]
 from boundforge.autoresearch.trace import Trace
 events=Trace(chosen).events
 for name,sha in report["artifact_hashes"].items():
  if hashlib.sha256((chosen/name).read_bytes()).hexdigest()!=sha:raise ValueError("artifact integrity failure "+name)
 controls=json.loads((BASE/"controls-continuation/summary.json").read_text());source=[e["data"]for e in events if e["kind"]=="exa_frontier_gate"][-1];model=[e["data"]for e in events if e["kind"]=="tinker_operator_proposal"]
 assert report["status"]=="certified_historical_replay"and len(report["experiments"])>=2
 gain=F(report["accepted"]["strict_gain_lower"]);assert gain>F(158,10**19)
 rows=[{"name":"Bernstein polynomial","nodes":report["accepted"]["checkers"]["c51_bernstein.py"]["nodes"]},{"name":"Direct trig / Taylor","nodes":report["accepted"]["checkers"]["c51_taylor.py"]["nodes"]},{"name":"Published decimal checker","nodes":report["accepted"]["published_checker"]["cover"]["nodes"]}]
 return {"report":report,"candidate":candidate,"events":events,"controls":controls,"pretty_bound":decimal(candidate["lower_bound"]),"previous_upper":decimal(report["accepted"]["previous_actual_beta_upper"],24,True),"checker_rows":rows,"source_entries":source["source_entries"],"source_confirmed":source["registered_witness_confirmed"],"request_ids":source["request_ids"],"model_event":model[-1]if model else None,"scope":"Historical artifact replay. Initial discovery agent-directed; no held-out or general-method advantage claim."}
def font(size,bold=False,mono=False):
 p="/usr/share/fonts/truetype/dejavu/DejaVuSans"+("Mono"if mono else"")+("-Bold"if bold else"")+".ttf"
 return ImageFont.truetype(p,size)
def wrap(draw,text,fo,width):
 words=text.split();lines=[];line=""
 for word in words:
  trial=(line+" "+word).strip()
  if draw.textlength(trial,font=fo)<=width:line=trial
  else:
   if line:lines.append(line)
   while draw.textlength(word,font=fo)>width:
    k=len(word)
    while draw.textlength(word[:k],font=fo)>width:k-=1
    lines.append(word[:k]);word=word[k:]
   line=word
 if line:lines.append(line)
 return lines
def frame(i,title,rows,foot):
 im=Image.new("RGB",(1280,720),"#102d2c");d=ImageDraw.Draw(im);d.rounded_rectangle((38,30,1242,690),radius=24,fill="#f5f5ed")
 d.text((72,50),"BOUNDFORGE  /  TRACK1  /  ACTUAL-ARTIFACT REPLAY",font=font(17,bold=True),fill="#26745c")
 d.text((1140,50),str(i+1)+" / 8",font=font(17,mono=True),fill="#546d65")
 y=99
 for line in wrap(d,title,font(42,bold=True),1120):
  d.text((72,y),line,font=font(42,bold=True),fill="#102d2c");y+=54
 y=max(y+20,208)
 for text,kind in rows:
  size=40 if kind=="big"else26 if kind=="mono"else23 if kind=="small"else28
  fo=font(size,bold=kind=="big",mono=kind=="mono");color="#147a58"if kind=="big"else"#ad5a18"if kind=="warning"else"#233c37"
  for line in wrap(d,text,fo,1120):
   d.text((72,y),line,font=fo,fill=color);y+=size+11
  y+=8
 if y>606:raise ValueError("scene text overflow "+str(i)+" "+str(y))
 d.line((72,622,1206,622),fill="#c6d3c7",width=2)
 for j,line in enumerate(wrap(d,foot,font(18),1120)[:2]):d.text((72,640+j*24),line,font=font(18),fill="#546d65")
 path=OUT/("frame-"+str(i)+".png");im.save(path);return path
def main():
 OUT.mkdir(parents=True,exist_ok=True);data=load();payload=json.dumps(data,ensure_ascii=True).replace("<","\\u003c");(OUT/"index.html").write_text(HTML.replace("__DATA__",payload))
 (OUT/"actual-data.json").write_text(json.dumps(data,indent=2))
 action=data["model_event"]["result"]["action"]if data["model_event"]else"precision_equioscillation"
 partial=decimal(data["report"]["verified_reference_improvements"][0]["lower_bound"])
 med=data["controls"]["medians"]
 scenes=[
 ("Research you can inspect",[( "C51a > "+data["pretty_bound"],"big"),("A bounded system chooses experiments, measures outcomes and requires mathematical certificates.","body"),("2 experiments • "+format(data["report"]["elapsed_seconds"],".2f")+" seconds in this recorded run","mono")],"Recorded execution is slowed for explanation. Initial finding: agent-directed research; this is an autonomous replay."),
 ("Use the full-precision frontier",[("Merged table: 0.5850788","mono"),("Actual prior-function upper: "+data["previous_upper"],"mono"),("The comparison uses the exact external witness, not the short headline.","body")],"Source: working report w042 and the public frontier audit. No external peer-review endorsement is implied."),
 ("Valid progress can still be below goal",[("Float proposal: "+partial,"mono"),("Existing project goal: 0.585078819674513590","mono"),("Retain the verified improvement. Retrieve its scoped record. Continue.","body")],"A smaller valid improvement is not mislabeled as a mathematical failure."),
 ("The next action comes from evidence",[("Selected operator: "+action,"mono"),("The controller reads its measured result and asks for a bounded next action.","body"),("Worker: no network, credentials, saved winner or repository mount.","body")],"Model explanations are unverified suggestions; they do not decide mathematical validity."),
 ("Exa is inside the research loop",[("Search excerpt: rounded result only.","body"),("Contents: exact K and alpha recovered.","body"),("Source gate: confirmed -> permit the next experiment.","body"),("Actual Exa cost for this run: $0.005","mono")],"Request IDs and source URLs are preserved. Full third-party documents are not republished."),
 ("Candidates cannot certify themselves",[(r["name"]+": PASS ("+str(r["nodes"])+" nodes)","body")for r in data["checker_rows"]]+[("Whole circle + exact infinite-tail bound.","body")],"Two own algorithms plus an unchanged separately authored decimal verifier. No numerical score accepts a record."),
 ("Strong controls remain in the report",[("Fixed high precision: "+format(med["fixed_precision"]["loop_wall_seconds"],".2f")+" s median","mono"),("Diagnostic controller: "+format(med["diagnostic"]["loop_wall_seconds"],".2f")+" s median","mono"),("Three paired seeds, one incumbent. No controller advantage demonstrated.","body")],"Identical maximum allowances; actual resource costs reported. Seeds do not establish broad generalization."),
 ("A real, very small refinement",[("Certified external-function gain > 1.58 × 10^-17","big"),("Runnable loop. Exact artifacts. Inspectable decisions.","body"),("Conventional search; no new general-method claim.","body"),("github.com/howdymary/boundforge","mono")],"Historical replay after agent-led discovery. The extremely small margin is a competitive limitation.")
 ]
 paths=[frame(i,*s)for i,s in enumerate(scenes)];playlist=OUT/"frames.txt"
 playlist.write_text("".join("file '"+str(p.resolve())+"'\nduration 15\n"for p in paths)+"file '"+str(paths[-1].resolve())+"'\n")
 movie=OUT/"boundforge-2min.mp4"
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(playlist),"-vf","fps=30,format=yuv420p","-t","120","-c:v","libx264","-preset","medium","-crf","22","-movflags","+faststart",str(movie)],check=True,timeout=240)
 probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=width,height,codec_name,r_frame_rate","-of","json",str(movie)]));assert abs(float(probe["format"]["duration"])-120)<.05
 manifest={"source_run":data["report"]["run_id"],"source_sha":data["report"]["source_sha"],"video":probe,"files":{p.name:{"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}for p in OUT.iterdir()if p.is_file()and p.name!="media-manifest.json"},"scope":"Silent captioned artifact-driven replay, not a live screen recording. No paid APIs during rendering."}
 (OUT/"media-manifest.json").write_text(json.dumps(manifest,indent=2));print(json.dumps({"video_bytes":movie.stat().st_size,"probe":probe}))
if __name__=="__main__":main()
