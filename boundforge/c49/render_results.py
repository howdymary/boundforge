"""Offline replay from actual immutable results; plots are standalone SVGs."""
import json,pathlib
def render(out,ev,tr,rows,check,usage):
 import matplotlib
 matplotlib.use("Agg")
 import matplotlib.pyplot as plt
 arms=["fixed","scheduled","ucb","no_memory","full","numeric","shuffled"]
 for filename,report in [("comparison.svg",ev),("transfer.svg",tr)]:
  tasks=list(report["summaries"]);fig,axs=plt.subplots(1,len(tasks),figsize=(3.1*len(tasks),4.5),squeeze=False)
  for ax,task in zip(axs[0],tasks):
   rr=[r for r in rows if r["task"]==task]
   means=[report["summaries"][task][a]["mean"] for a in arms]
   ax.bar(range(7),means,color=["#b5bec5" if a!="full" else "#a56b27" for a in arms],alpha=.8)
   for i,arm in enumerate(arms):
    ys=[r["best_score"] for r in rr if r["arm"]==arm]
    ax.scatter([i]*len(ys),ys,s=10,color="#203b48",alpha=.65,zorder=3)
   low=min(r["best_score"] for r in rr);high=max(r["best_score"] for r in rr);pad=max((high-low)*.2,.01 if high<2 else .5)
   ax.set_ylim(low-pad,high+pad);ax.set_title(task);ax.set_xticks(range(7),["fixed","schedule","UCB","no mem","full","numeric","shuffle"],rotation=60,ha="right");ax.grid(axis="y",alpha=.2)
  fig.suptitle("Recorded final outcomes: bars = means, dots = seven starts per arm\nNo pooled objective; repeated starts are not independent problem instances",fontsize=12)
  fig.tight_layout(rect=(0,0,1,.88));fig.savefig(out/filename);plt.close(fig)
 compact=[]
 for r in rows:
  compact.append({k:r[k] for k in ["task","kind","n","param","arm","seed","initial_score","warm_score","best_score","best_family","ports","cpu_seconds","tested"]}|{"trace":[{k:t[k] for k in ["step","diagnosis","next_diagnosis","action","decision","best_score","reward","cpu_seconds","tested","rejected","pair_rejected","triple_rejected","last_conflict","before_hash","after_hash"]} for t in r["trace"]]})
 payload=json.dumps({"rows":compact,"primary":ev,"followup":tr,"certification":check,"usage":usage},separators=(",",":")).replace("<","\\u003c")
 html="""<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BoundForge | C49a recorded evidence</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f6f4ef;color:#20323c;font:16px/1.55 system-ui,sans-serif;overflow-wrap:anywhere}main{max-width:1160px;margin:auto;padding:32px 22px 70px}header{border-top:5px solid #a56b27;padding-top:18px}h1{font-size:clamp(30px,5vw,52px);line-height:1.12;margin:10px 0}h2{font-size:23px;margin:0 0 12px}.eyebrow{color:#75501e;font-size:12px;text-transform:uppercase;letter-spacing:.12em}p{max-width:90ch}.lead{font-size:19px}section{margin-top:30px;padding:23px;background:white;border:1px solid #d9dedc;border-radius:12px;min-width:0}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.metric{padding:15px;background:#f3f6f4;border-radius:8px}.metric strong{display:block;font-size:25px}.muted{color:#5a6c73;font-size:14px}.tag{display:inline-block;background:#f5e9d8;color:#774e19;padding:5px 10px;border-radius:5px;font-weight:650}.controls{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}select{width:100%;max-width:100%;padding:9px;font:inherit;border:1px solid #a8b9bd;border-radius:5px;background:white}label{display:block;font-size:14px;min-width:0}.scroll{overflow:auto;max-width:100%}table{border-collapse:collapse;width:100%;font-size:13px;min-width:560px}td,th{text-align:left;padding:9px;border-bottom:1px solid #e2e7e7}th{background:#f3f6f4}.chart{width:100%;height:auto;display:block}.chart svg{width:100%;height:auto;display:block}pre{font-size:12px;white-space:pre-wrap;word-break:break-word;max-height:330px;overflow:auto;background:#eef3f3;padding:14px;border-radius:6px}button,.button{font:inherit;display:inline-block;border:0;border-radius:5px;background:#244b59;color:white;padding:9px 14px;cursor:pointer;text-decoration:none}a{color:#245f78}details{margin-top:12px}canvas{max-width:100%;width:100%;height:170px;background:#f6f9f8;border-radius:7px}.links{display:flex;gap:10px;flex-wrap:wrap}footer{margin-top:26px;font-size:13px;color:#5a6c73}@media(max-width:600px){main{padding:22px 14px}.grid,.controls{grid-template-columns:minmax(0,1fr)}section{padding:17px}.lead{font-size:17px}}
</style><main>
<header><div class="eyebrow">Computational mathematics · recorded campaign · November 2026</div><h1>BoundForge / C49a</h1><p class="lead">A research loop with exact acceptance, matched comparisons, and an honest negative result.</p><span class="tag">No new record · no demonstrated controller advantage</span></header>
<section><h2>The strongest verified witness is prior art</h2><div class="grid"><div class="metric"><strong>1.56786438457…</strong>Reproduced lower bound</div><div class="metric"><strong>252,303</strong>Sets on 28 ground points</div><div class="metric"><strong>2 + 2</strong>Own final algorithms + primary replay checkers</div></div><p>Witness credit: Pinho and collaborators, PR370, building on the earlier construction literature. The merged table entry is weaker. BoundForge reproduced the stronger open claim and did not improve it.</p><p class="muted">Counts [33980,64728,64728,88867]; transfer matrix [[64728,88867],[33980,64728]]; rate (64728+√3019700660)^(1/26). Exact checkers establish Sperner, sunflower-freeness and ports; the documented gluing proof gives the asymptotic implication.</p><div class="links"><a class="button" href="baseline.json" download>Exact baseline data</a><a href="certification.json">Fresh certification</a><a href="../RESEARCH_DESIGN.md">Proof and design</a><a href="https://github.com/teorth/optimizationproblems/pull/370">Original open claim</a></div><details><summary>Inspect certification</summary><pre id="certificate"></pre></details></section>
<section><h2>Matched primary comparison</h2><p>245 episodes; seven arms; five tasks; seven paired starts per task. Equal six-operator libraries and 6.25 process-CPU seconds per episode. Full used the frozen numerical fallback: this was not a held-out test of model-written policies.</p>
<p>The full controller trailed scheduled and numerical selection on uniform9. Four tasks hit identical outcomes across arms. Repeated starts do not establish broad transfer or statistical independence.</p>
<img class="chart" src="comparison.svg" alt="Per-task final objective means and individual recorded starts for seven controllers">
<div class="scroll" id="summary"></div><details><summary>Post-hoc harder transfer diagnostic</summary><p>Unchanged controller and operators; new auxiliary tasks. These results supplement, and do not replace, the frozen primary comparison.</p><img class="chart" src="transfer.svg" alt="Harder auxiliary follow-up final outcomes"><div class="scroll" id="transfer"></div></details></section>
<section><h2>Replay an actual decision chain</h2><p class="muted">No live APIs or simulated improvement. Each line comes from a saved episode. Archive reads are aggregate action-reward statistics; changed actions and later gains do not prove memory caused a gain.</p><div class="controls"><label>Task<select id="task"></select></label><label>Controller<select id="arm"></select></label><label>Paired seed<select id="seed"></select></label></div><p id="episode"></p><canvas id="curve" width="960" height="170" aria-label="Recorded best objective by decision step"></canvas><div class="scroll"><table><thead><tr><th>Step</th><th>Diagnosis</th><th>Action</th><th>Best objective</th><th>Tested / rejected</th><th>Archive context</th></tr></thead><tbody id="trace"></tbody></table></div><div class="links" style="margin-top:14px"><button id="download">Download exact episode witness</button></div><p class="muted" id="witness"></p><details><summary>Raw selected decision evidence</summary><pre id="decision"></pre></details></section>
<section><h2>Costs and claim boundaries</h2><div class="scroll" id="usage"></div><p class="muted">Amounts include unresolved conservative reservations; they are not final invoices. Historical holds are separate. No GPUs, fine-tuning, credit purchases or leaderboard submissions. Four later Tinker samples produced two valid development rules, both below the numerical rule.</p><p>Production CP-SAT and periodic-gluing searches found no improved witness. Timeouts, sampled failures and failed common-vector inequalities do not certify impossibility. The next justified campaign needs a different construction or a better discriminating benchmark.</p><div class="links"><a href="../FINAL_RESEARCH_REPORT.md">Full assessment</a><a href="manifest.json">Artifact hashes</a><a href="provenance.json">Executed source revisions</a><a href="provider-usage.json">Reservation ledger</a></div></section>
<footer>Recorded-artifact replay. Exact certification must be run through the independent Python/C++ checkers; this browser only shows data, counts and provenance.</footer>
</main><script id="data" type="application/json">PAYLOAD</script><script>
"use strict";
var D=JSON.parse(document.getElementById("data").textContent),selected;
var task=document.getElementById("task"),arm=document.getElementById("arm"),seed=document.getElementById("seed");
function fmt(x){return typeof x==="number"?Number(x.toPrecision(11)).toString():String(x)}
function esc(s){return String(s).replace(/[&<>"]/g,function(x){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[x]})}
function options(el,values,initial){el.innerHTML=values.map(function(x){return '<option value="'+esc(x)+'">'+esc(x)+'</option>'}).join("");if(initial!==undefined)el.value=String(initial)}
function summary(report,id){var aa=["fixed","scheduled","ucb","no_memory","full","numeric","shuffled"];document.getElementById(id).innerHTML="<table><thead><tr><th>Task</th>"+aa.map(function(a){return "<th>"+esc(a)+"</th>"}).join("")+"</tr></thead><tbody>"+Object.keys(report.summaries).map(function(t){return "<tr><td>"+esc(t)+"</td>"+aa.map(function(a){return "<td>"+fmt(report.summaries[t][a].mean)+"</td>"}).join("")+"</tr>"}).join("")+"</tbody></table>"}
summary(D.primary,"summary");summary(D.followup,"transfer");
document.getElementById("usage").innerHTML="<table><tr><th>Provider</th><th>Actual or reserved</th><th>Unresolved</th><th>Campaign cap</th></tr>"+Object.keys(D.usage).map(function(p){var u=D.usage[p];return "<tr><td>"+p+"</td><td>"+fmt(u.reserved_or_actual)+" "+u.unit+"</td><td>"+fmt(u.unresolved_holds)+"</td><td>"+u.campaign_cap+"</td></tr>"}).join("")+"</table>";
document.getElementById("certificate").textContent=JSON.stringify(D.certification,null,2);
options(task,Array.from(new Set(D.rows.map(function(r){return r.task}))),"uniform9");
options(arm,["fixed","scheduled","ucb","no_memory","full","numeric","shuffled"],"full");
options(seed,[410,420,430,440,450,460,470],410);
var actions=["remove 2","remove 6","large ruin","restart","conflict-guided","structure-guided"];
function draw(r){var cv=document.getElementById("curve"),ctx=cv.getContext("2d"),ys=[r.warm_score].concat(r.trace.map(function(t){return t.best_score})),lo=Math.min.apply(null,ys),hi=Math.max.apply(null,ys),span=hi-lo||.01;
ctx.clearRect(0,0,960,170);ctx.strokeStyle="#a56b27";ctx.lineWidth=3;ctx.beginPath();ys.forEach(function(y,i){var x=55+i*875/(ys.length-1),v=140-(y-lo)*110/span;if(i===0)ctx.moveTo(x,v);else ctx.lineTo(x,v)});ctx.stroke();ctx.fillStyle="#20323c";ctx.font="13px system-ui";ctx.fillText(fmt(hi),8,20);ctx.fillText(fmt(lo),8,155);ctx.fillText("warmup → 24 bounded decisions",620,160)}
function refresh(){selected=D.rows.find(function(r){return r.task===task.value&&r.arm===arm.value&&String(r.seed)===seed.value});if(!selected)return;var r=selected;
document.getElementById("episode").textContent=r.task+" · "+r.arm+" · seed "+r.seed+" · final "+fmt(r.best_score)+" · "+fmt(r.cpu_seconds)+" CPU seconds · "+r.tested.toLocaleString()+" tests";
document.getElementById("trace").innerHTML=r.trace.map(function(t){return "<tr><td>"+t.step+"</td><td>"+esc(t.diagnosis)+"</td><td>"+actions[t.action]+"</td><td>"+fmt(t.best_score)+"</td><td>"+t.tested+" / "+t.rejected+"</td><td>"+esc(t.decision.context_read||t.decision.policy)+"</td></tr>"}).join("");
document.getElementById("decision").textContent=JSON.stringify(r.trace.filter(function(t){return t.decision.policy==="empirical context UCB"&&t.decision.choice_differs_from_fixed}).slice(0,3),null,2);
var counts=r.kind===0?[0,0,0,0]:null;if(counts)r.best_family.forEach(function(x){counts[2*((x>>r.ports[0])&1)+((x>>r.ports[1])&1)]++});
document.getElementById("witness").textContent=r.kind===0?"Exact masks: "+r.best_family.length+"; ground points "+r.n+"; ports "+r.ports.join(",")+"; browser-counted cells "+counts.join(",")+". Validity is recorded in the independent checker artifacts.":"Exact task witness has "+r.best_family.length+" members. Its task-specific validity was checked in the saved evaluation.";
draw(r)}
[task,arm,seed].forEach(function(el){el.addEventListener("change",refresh)});
document.getElementById("download").addEventListener("click",function(){var r=selected,obj=r.kind===0?{n:r.n,ports:r.ports,masks:r.best_family,source:{task:r.task,arm:r.arm,seed:r.seed},scope:"Recorded finite witness; not a new record"}:{task:r.task,kind:r.kind,n:r.n,param:r.param,members:r.best_family};var url=URL.createObjectURL(new Blob([JSON.stringify(obj,null,2)],{type:"application/json"})),a=document.createElement("a");a.href=url;a.download="boundforge-"+r.task+"-"+r.arm+"-"+r.seed+".json";a.click();setTimeout(function(){URL.revokeObjectURL(url)},1000)});
refresh();
</script></html>"""
 # Standalone, offline HTML retains figures inline while separate SVGs remain exportable.
 for name in ["comparison.svg","transfer.svg"]:
  svg=(out/name).read_text();svg=svg[svg.index("<svg"):]
  html=html.replace('<img class="chart" src="'+name+'" alt="'+("Per-task final objective means and individual recorded starts for seven controllers" if name=="comparison.svg" else "Harder auxiliary follow-up final outcomes")+'">','<div class="chart">'+svg+'</div>')
 html=html.replace("PAYLOAD",payload)
 (out/"demo.html").write_text(html)
