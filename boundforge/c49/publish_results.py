"""Collect immutable remote artifacts, certify afresh, and preserve an honest report.
Runs only on an ephemeral GitHub runner. No paid calls or leaderboard submissions.
"""
import collections,datetime,hashlib,io,json,math,os,pathlib,random,sqlite3,statistics,subprocess,sys,time,zipfile
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1];OUT=HERE/"results";OUT.mkdir(exist_ok=True)
REPO=os.environ.get("GITHUB_REPOSITORY","howdymary/boundforge")
RUNS={"stage_a":43678845982,"pilot":43679514101,"freeze":43679935507,"evaluation":43680044118,"model_study":43680369383,"production":43680657530,"transfer":43680750855,"ports":43681053247}
PROTECTED={"boundforge/verify.py":"3c5cd73bf3d50eea098d3253e46e9e5ea9812ec3c2fa2711ea16b349f586ef30","boundforge/verify_independent.py":"49e1cbbc9d287a227d8f790b2f7a678972a88f53d3c2e88592f6c1424dda0774"}
def api(path,method="GET",body=None,raw=False):
 cmd=["gh","api","repos/"+REPO+"/"+path]
 if method!="GET":cmd+=["--method",method,"--input","-"]
 q=subprocess.run(cmd,input=None if body is None else json.dumps(body).encode(),capture_output=True,check=True)
 return q.stdout if raw else json.loads(q.stdout)
def put(path,data):
 p=OUT/path;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes(data if isinstance(data,bytes) else (json.dumps(data,indent=2,ensure_ascii=False)+"\n").encode())
def archive(run):
 info=api("actions/runs/"+str(run));assert info["conclusion"]=="success",(run,info["conclusion"])
 items=api("actions/runs/"+str(run)+"/artifacts")["artifacts"];assert len(items)==1
 a=items[0];raw=api("actions/artifacts/"+str(a["id"])+"/zip",raw=True)
 return zipfile.ZipFile(io.BytesIO(raw)),{"run":run,"source_sha":info["head_sha"],"artifact":a["name"],"artifact_id":a["id"],"zip_sha256":hashlib.sha256(raw).hexdigest(),"started":info["run_started_at"],"updated":info["updated_at"]}
def paired(rows):
 out={}
 for task in sorted({r["task"] for r in rows}):
  rr=[r for r in rows if r["task"]==task];arms=sorted({r["arm"] for r in rr});full={r["seed"]:r["best_score"] for r in rr if r["arm"]=="full"};out[task]={}
  for arm in arms:
   other={r["seed"]:r["best_score"] for r in rr if r["arm"]==arm}
   d=[full[s]-other[s] for s in sorted(full)];rng=random.Random(9742)
   boot=sorted(statistics.mean(rng.choices(d,k=len(d))) for _ in range(5000))
   out[task][arm]={"full_minus_arm":d,"mean":statistics.mean(d),"min":min(d),"max":max(d),"paired_start_sd":statistics.stdev(d) if len(d)>1 else 0,"bootstrap95_start_only":[boot[124],boot[4874]],"scope":"Conditional resampling of seven starts on this single task, not independent problem-level generalization; no multiplicity correction."}
 return out
def table(report):
 lines=["| Task | Fixed | Scheduled | Global UCB | No memory | Full | Numerical | Shuffled |","|---|---:|---:|---:|---:|---:|---:|---:|"]
 for name,arms in report["summaries"].items():lines.append("|"+name+"|"+"|".join(format(arms[a]["mean"],".10g") for a in ["fixed","scheduled","ucb","no_memory","full","numeric","shuffled"])+"|")
 return "\n".join(lines)
def main():
 start=time.monotonic();provenance={};archives={};allrows={}
 for phase,run in RUNS.items():
  z,pr=archive(run);archives[phase]=z;provenance[phase]=pr
  for name in z.namelist():
   if "/" in name or not name.endswith((".json",".jsonl")) or name=="exa-working.json":continue
   raw=z.read(name)
   if phase=="stage_a" and name=="frontier.json":
    data=json.loads(raw)
    def redact(x):
     if isinstance(x,dict):return {k+("_sha256" if k=="body" else ""):(hashlib.sha256(str(v).encode()).hexdigest() if k=="body" else redact(v)) for k,v in x.items()}
     if isinstance(x,list):return [redact(v) for v in x]
     return x
    raw=(json.dumps(redact(data),indent=2)+"\n").encode()
   if name=="episodes.json":
    rows=json.loads(raw);allrows[phase]=rows
    for task in sorted({r["task"] for r in rows}):
     for arm in sorted({r["arm"] for r in rows}):
      put(phase+"/episodes/"+task+"/"+arm+".json",[r for r in rows if r["task"]==task and r["arm"]==arm])
    put(phase+"/episodes-index.json",{"episodes":len(rows),"original_sha256":hashlib.sha256(raw).hexdigest(),"layout":"episodes/TASK/ARM.json","tasks":sorted({r["task"] for r in rows})})
   else:put(phase+"/"+name,raw)
  report=json.loads(z.read("report.json")) if "report.json" in z.namelist() else None
  if phase in ("evaluation","transfer"):put(phase+"/paired-effects.json",paired(allrows[phase]))
  if report and report.get("new_record"):raise RuntimeError("New candidate requires dedicated record certification/review before summary publication")
 # Preserve only mathematical witness data, not transient copies of external code.
 basepath=next(n for n in archives["stage_a"].namelist() if n.startswith("replay/certificates/best_") and n.endswith(".json"))
 raw=archives["stage_a"].read(basepath)
 assert hashlib.sha256(raw).hexdigest()=="53381b5f52264c43d56343ab27d698c598462d5abfd83c043365afbae9efb1e8"
 put("baseline.json",raw)
 from certify import certify
 before=time.monotonic();finalcheck=certify(OUT/"baseline.json",OUT/"baseline.json")
 finalcheck["wall_seconds"]=time.monotonic()-before
 finalcheck["scope"]="Reproduction of Pinho PR370, not a new BoundForge construction. Fresh own Cartesian-box and C++ BDD implementations; primary checker replays are in stage_a."
 assert finalcheck["valid"] and not finalcheck["strict_improvement"]
 put("certification.json",finalcheck)
 for path,digest in PROTECTED.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,("protected file changed",path)
 # Refresh frontier through read-only GitHub, no paid call.
 pull=api("https://api.github.com/repos/teorth/optimizationproblems/pulls/370") if False else json.loads(subprocess.check_output(["gh","api","repos/teorth/optimizationproblems/pulls/370"]))
 put("frontier-refresh.json",{k:pull.get(k) for k in ["html_url","number","state","merged","merged_at","updated_at","head","base"]})
 # Ledger preserves unknown provider charges as holds; do not convert allowances to invoices.
 db=sqlite3.connect(":memory:");db.deserialize(archives["transfer"].read("budget.sqlite"))
 records=[dict(zip(["id","provider","amount","actual","label"],r)) for r in db.execute("select id,provider,amount,actual,label from reservations")]
 snapshot=json.loads((HERE/"campaign-budget.json").read_text())
 usage={}
 for provider,s in snapshot["providers"].items():
  rec=[r for r in records if r["provider"]==provider]
  usage[provider]={"unit":"credits" if provider=="past" else "USD","campaign_cap":s["campaign_cap"],"settled_receipts_or_api_estimates":sum(r["actual"] or 0 for r in rec),"unresolved_holds":sum(r["amount"] for r in rec if r["actual"] is None),"reserved_or_actual":sum(r["amount"] if r["actual"] is None else r["actual"] for r in rec),"historical_hold_separate":s["old_hold"],"external_pending_guard":s["external_pending_guard"],"note":"Modal holds are conservative reservations, not metered cost. past entries use API estimates/recall charge assumptions. Tinker token estimates are separate from unresolved call allowances."}
  assert usage[provider]["reserved_or_actual"]<=s["campaign_cap"]
 put("provider-usage.json",{"providers":usage,"reservations":records,"snapshot":"../campaign-budget.json","billing_reconciliation":"No post-campaign dashboard invoice reconciliation available; unresolved holds retained. No credits purchased, replenishment enabled, upgrades, or GPUs used."})
 ev=json.loads(archives["evaluation"].read("report.json"));tr=json.loads(archives["transfer"].read("report.json"));prod=json.loads(archives["production"].read("report.json"));ports=json.loads(archives["ports"].read("report.json"));model=json.loads(archives["model_study"].read("report.json"))
 # Actual aggregate-archive reads and outcomes; this is not a causal memory advantage.
 fr=json.loads(archives["freeze"].read("freeze.json"));chains=[]
 for r in allrows["evaluation"]:
  if r["arm"]!="full":continue
  prev=r["warm_score"]
  for t in r["trace"]:
   d=t["decision"]
   if d.get("policy")=="empirical context UCB" and d.get("choice_differs_from_fixed") and t["best_score"]>prev+1e-14:
    chains.append({"task":r["task"],"seed":r["seed"],"step":t["step"],"retrieved_aggregate_archive":{"source_paired_sha256":fr["paired_archive_sha256"],"context":d["context_read"],"counts":d["archive_counts"]},"decision":d,"action_executed":t["action"],"before_hash":t["before_hash"],"after_hash":t["after_hash"],"objective_before":prev,"objective_after":t["best_score"],"measured_evidence":{"tested":t["tested"],"rejected":t["rejected"],"pair_rejected":t["pair_rejected"],"triple_rejected":t["triple_rejected"],"last_conflict":t["last_conflict"]},"scope":"Read aggregate contextual rewards, chose differently from fixed baseline, executed action, measured gain. Does not show this exact gain was caused by persistent memory."})
   prev=t["best_score"]
 put("memory-decision-chains.json",{"chains":chains[:12],"qualifying_chain_count":len(chains),"hosted_memory_claim":"Two roles wrote/read past.dev; asymmetric source retrieval and no demonstrated past.dev-specific outcome advantage."})
 rows=allrows["evaluation"]+allrows["transfer"]
 totals={"evaluation_cpu_seconds":ev["episodes"]*6.25,"transfer_cpu_seconds":tr["episodes"]*6.25,"pilot_cpu_seconds_including_probes":42,"production_cpu_seconds":prod["cpu_seconds"],"candidate_evaluations":sum(r["tested"] for r in rows),"gpu_seconds":0,"model_training":0,"model_samples":4,"valid_model_samples":model["valid_rules"],"model_token_cost_estimate_usd":0.0185256,"certification_wall_seconds":finalcheck["wall_seconds"],"evaluation_elapsed_seconds":ev["elapsed_seconds"],"transfer_elapsed_seconds":tr["elapsed_seconds"],"ports_elapsed_seconds":ports["elapsed_seconds"]}
 put("resource-summary.json",totals)
 # Record final source hashes without pretending all phases ran this same revision.
 put("provenance.json",{"collected_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"collection_source_sha":os.environ["GITHUB_SHA"],"source_runs":provenance,"protected_hashes":PROTECTED,"failures":[{"run":43679239618,"reason":"Initial image C++ name collision; conservative image hold retained"},{"run":43679314789,"reason":"Free runner caught same compiler error"},{"run":43679427482,"reason":"Pytest relative import"},{"run":43679780777,"reason":"Tokenizer Jinja dependency, memory polling; partial Exa/past usage recovered"},{"run":43679935507,"reason":"Successful numerical fallback; Tinker billing datetime schema rejected calls before inference"}],"notes":["Full Exa source text and transient external checker code/binaries are not republished.","Each phase retains its executed source SHA; later engineering fixes do not retroactively change frozen evaluation."]})
 text="""# C49a campaign assessment

Research date: November14,2026 America/Los_Angeles; runs and collection November15 UTC.

**No new C49a lower bound and no demonstrated new general research method.** The strongest retained result is an independent reproduction of a prior open claim, not a BoundForge record. The hypotheses were tested rather than declared successful.

## Frontier and certification

The reproduced incumbent is [PR370](https://github.com/teorth/optimizationproblems/pull/370), pinned to [Pinho's certificate packet](https://github.com/rpinho/math-certificates/tree/a50021b04687719f4a2ea27609029982c980573e/c49/round1). Its rate is
(64728+sqrt(3019700660))^(1/26) = 1.567864384572806979362033445047060687289228710864066381805835...
on a 252303-member Sperner sunflower-free family on28 points with ports0,1. Port counts are [33980,64728,64728,88867]. The weaker merged Koshta table value is 1.56785990242458988585...; beating that alone would not establish a new record.

StageA replayed both primary checkers and our BDD implementation. Final certification freshly executes our own Cartesian-box and BDD implementations, agrees on all counts, checks every required finite property and isolates the rate using exact rationals. These independently implemented algorithms were written after reading primary sources, not claimed clean-room. See [certification](results/certification.json), [exact baseline](results/baseline.json), [frontier audit](results/stage_a/frontier.json), [refresh](results/frontier-refresh.json), [source hashes](results/stage_a/sources.json), and [proof/specification](RESEARCH_DESIGN.md). The original1997 publisher typeset proof was inaccessible; operative complete gluing proofs in Koshta/Pinho were inspected. Prior authors retain credit.

An accessible witness is not proof no newer unpublished claim exists. The frontier audit distinguishes merged entry, open claim, and independently reproduced witness. No external leaderboard was updated.

## Experiment outcomes

The development pilot used24 saved-state/seed comparisons: a common250ms probe followed by six paired250ms interventions,42CPU seconds total. F10 remained flat. Uniform8 favored removal6 and conflict-guided repair. Two families and their deletions do not provide a broad learning distribution.

The frozen primary study used245 episodes, seven arms, five held-out tasks and seven paired starts per task. Each arm had the same six operators and6.25CPU seconds per episode, including warmup. Tinker was disabled at freeze by its failed billing probe; the full arm therefore used the frozen **numerical fallback**, not a model-written policy. Archived trace wording saying "model rule" is a labeling limitation.

""" + table(ev) + """

On uniform9, full improves over the development-selected fixed procedure, but scheduled switching and numerical contextual selection both do better. Four other primary tasks have identical final results across all arms, so those ceiling results are uninformative about relative discovery quality. This does not establish diagnostic or memory superiority. Seven starts are dependent repetitions on a single family, not seven independent mathematical tasks.

A separately registered **post-hoc** harder auxiliary follow-up kept controller/engine hashes unchanged. It is a ceiling diagnostic, not a replacement of the primary study or evidence the original benchmark was adequate.

""" + table(tr) + """

Raw episodes, exact checks, per-phase resource summaries and paired differences are in [primary results](results/evaluation/report.json) and [follow-up results](results/transfer/report.json). Paired bootstrap ranges resample starts only; no problem-level confidence or multiplicity-adjusted significance is claimed. Different task objectives are never pooled into one score.

Four later Tinker proposals were tested only on development data: two failed the strict integer-action schema and two were valid. Their expected rewards (0.0077916315 and0.0075969703) were below the numerical rule (0.0083885031). No fine-tuning was justified or run. The model study neither repairs nor changes frozen held-out results.

Production switched from stalled greedy repair to classical CP-SAT whole-family search, with exact containment constraints, valid separated sunflower clauses and sufficient rational Collatz inequalities. Six bounded configurations covered n10/n11 and different Perron-vector ratios. """ + str(sum(x["candidate_found"] for x in prod["outcomes"])) + """ valid candidates were found; none improved the incumbent. Solver UNKNOWN/timeouts are unsuccessful finite-budget attempts, not impossibility proofs. Any infeasible status has only its stated ratio restriction and no independently checked UNSAT certificate. Details: [production](results/production/report.json).

A separate free periodic-gluing search enumerated956 ordered port choices, deduplicated26 matrices, tested all matrix pairs and a width256 beam through period8. Exact comparison of the leading screened candidates found no record. The common-positive-vector hypothesis failed754 inequalities: it proves no exclusion and is retained as a failed diagnostic. Neither bounded beam search nor failed sampling rules out other compositions.

## Diagnostics, memory and limits

Measured rejection counts, exact state hashes, action choices, budgets, conflict examples and observed objectives support inspectable decision chains. [Memory examples](results/memory-decision-chains.json) link aggregate archive reads to changed actions and measured consequences. They do not establish a causal memory benefit. Development paired probes are the actual same-state intervention tests. Hosted past.dev source retrieval was asymmetric; a later role retrieved a controller record. No hosted-memory performance advantage is claimed.

Limitations: small development distribution; weak differentiation on ceiling tasks; coarse heuristic diagnosis labels; mismatch labels in episode logs lack their raw counter (pilot records retain it); no complete isomorphism reduction; no literal neighborhood-exhaustion certificate; per-family port counts for all intermediate states are not retained; fixed-controller selection is development-best, not globally strongest possible search. CPU equalization does not equal end-to-end inference cost. Final task adapters and several action heuristics are human designed.

The full controller is contextual UCB with a tiny ranking bias and aggregate rewards. That is close to adaptive operator selection/ALNS, not a newly discovered general method. [Novelty table](RESEARCH_DESIGN.md) and [memory prior art](PRIOR_ART_ADDENDUM.md) identify the overlap with Ropke/Pisinger, Fialho, Kotthoff, FunSearch, AlphaEvolve, PatternBoost, Reflexion and Voyager. The comparison fails to establish the intended advantage; additional terminology would not change that result.

## Resources, credit accounting and stopping

""" + "\n".join("- "+p+": "+str(round(v["reserved_or_actual"],6))+" "+v["unit"]+" campaign actual-or-reserved; "+str(round(v["unresolved_holds"],6))+" unresolved; historical hold "+str(v["historical_hold_separate"])+" separate." for p,v in usage.items()) + """

These are conservative ledger amounts, **not all final charges**. Exa receipts total0.063USD; Tinker token estimates total0.0185256USD within0.80USD held for four calls; Modal actual metered invoice is unresolved. past usage entries are reported in credits with API estimation caveats. Old holds and external-project guards remain separate. See [provider records](results/provider-usage.json), [resource summary](results/resource-summary.json), and the initial [billing snapshot](campaign-budget.json). No GPUs or training were needed.

The paid ledger was serialized across pilot, freeze, held-out evaluation, model component, production and follow-up. Unknown charges remain held; there were no purchases, auto-replenishment changes or upgrades. Final independent certification used GitHub Actions, outside paid provider experiments. No unsupported large batch is launched merely because credits remain.

The preregistered greedy direction stalled; controlled evaluation did not support scaling the full controller; bounded new-family CP-SAT and periodic compositions did not improve the record. Those tested directions stop here. This is a scoped negative campaign, not a proof the mathematical target is exhausted. A new campaign requires a materially different mathematical construction or a better discriminating benchmark, fresh budgets and a new freeze.

## Six separate contribution answers

1. **What mathematical result is new?** No improved C49a bound. The retained 1.56786438457... witness and gluing theorem are prior art. No new exclusion theorem was proved.
2. **What research mechanism is new?** None established relative to adaptive operator selection and agent-memory prior art. The concrete artifact is an adaptation with structured diagnostics and independent acceptance.
3. **What evidence shows it helps?** Full beats a weak development-selected fixed baseline on uniform9, but not scheduled/numerical controls. That does not establish the central hypothesis. The later model rules do worse on development.
4. **Where does it transfer or fail?** The same controller executes on independent sets and cap sets using human-designed adapters; raw follow-up results are above. Execution transfer does not establish a general performance benefit. C49 F/H constructions and most primary auxiliary instances stall.
5. **What remains standard engineering, adaptation or conjecture?** Exact verification, gluing/Perron analysis, CP-SAT separation, ALNS-like ruin/repair, contextual UCB, provider integrations and logging are standard methods or engineering adaptations. Reusable diagnosis-driven discovery advantage remains conjectural and unsupported here.
6. **Which Track1 criteria are met?** An autonomous bounded propose/evaluate/update loop and inspectable logs exist. **The record-beating objective is not met.** A new general research method has not been demonstrated. This is not ready to present as a winning or publishable mathematical advance.

Reproduction requires no paid service: run the remote C49 publication/check workflow or follow [the C49 guide](README.md). The [offline actual-artifact demo](results/demo.html) replays recorded outcomes; it does not run fresh inference or claim a simulated record.
"""
 (HERE/"FINAL_RESEARCH_REPORT.md").write_text(text)
 from render_results import render
 render(OUT,ev,tr,rows,finalcheck,usage)
 # Immutable artifact hashes; report/source hashes are not circularly included.
 manifest={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.rglob("*")) if p.is_file() and p.name!="manifest.json"}
 put("manifest.json",manifest)
 # Publish only this target's evidence. Preserve concurrent changes via fresh nonforced main ref.
 files=[p for p in OUT.rglob("*") if p.is_file()]+[HERE/"FINAL_RESEARCH_REPORT.md"]
 head=api("git/ref/heads/main")["object"]["sha"];tree=api("git/commits/"+head)["tree"]["sha"]
 entries=[]
 for p in files:
  content=p.read_text();blob=api("git/blobs","POST",{"content":content,"encoding":"utf-8"})
  entries.append({"path":str(p.relative_to(ROOT)),"mode":"100644","type":"blob","sha":blob["sha"]})
 newtree=api("git/trees","POST",{"base_tree":tree,"tree":entries})
 commit=api("git/commits","POST",{"message":"Preserve C49 negative campaign, exact baseline certification, matched comparisons and artifact replay","tree":newtree["sha"],"parents":[head]})
 api("git/refs/heads/main","PATCH",{"sha":commit["sha"],"force":False})
 print("C49_PUBLISHED "+json.dumps({"commit":commit["sha"],"files":len(files),"elapsed_seconds":time.monotonic()-start,"provider_allowances":usage}))
if __name__=="__main__":main()
