"""Read-only complete table inventory and declared practical-priority tiers."""
import base64,hashlib,io,json,os,pathlib,re,subprocess,tarfile
HERE=pathlib.Path(__file__).resolve().parent;OUT=HERE/"audit";OUT.mkdir(exist_ok=True)
def api(path):return json.loads(subprocess.check_output(["gh","api",path]))
def main():
 repo="teorth/optimizationproblems";head=api("repos/"+repo+"/commits/main")["sha"]
 raw=subprocess.check_output(["gh","api","repos/"+repo+"/tarball/"+head]);tar=tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz")
 pages={}
 for m in tar.getmembers():
  p=m.name.split("/",1)[-1]
  if m.isfile() and (p=="README.md" or p.startswith("constants/") and p.endswith(".md")):pages[p]=tar.extractfile(m).read().decode()
 prs=api("repos/"+repo+"/pulls?state=open&per_page=100")
 claims=[{"number":p["number"],"title":p["title"],"url":p["html_url"],"updated":p["updated_at"],"body_sha256":hashlib.sha256((p["body"]or"").encode()).hexdigest()} for p in prs]
 priority=["3e","3a","1b","1d","51a","89a","47a","82a","86a","1a","42a","1c","59a","57c","26a","26b","37a","9a","4a","45a","31a","38a","30a","16a","49a","3c"]
 solved={"2a","3d","11b","48a","83a"}
 finite={"13a","13b","15a","15b","22a","22b","23a","23b","23c","24a","27a","27b","28a","29a","36a","39a","41a","41b","43a","44a","50a","53a","68a","70a","71a","73a","75a","78a","80a","87a","90a"}
 rows=[]
 for path,text in pages.items():
  if not path.startswith("constants/"):continue
  ident=path.split("/")[-1][:-3];name=text.splitlines()[0].lstrip("# ")
  tier=0 if ident in priority else 9 if ident in solved else 3 if ident in finite else 5
  rank=priority.index(ident)+1 if ident in priority else None
  row={"id":ident,"name":name,"tier":tier,"priority_rank":rank,"url":"https://teorth.github.io/optimizationproblems/"+path.replace(".md",".html"),"source_sha256":hashlib.sha256(text.encode()).hexdigest(),"page_bytes":len(text.encode()),"status":"excluded: recorded as solved" if ident in solved else "priority pilot, frontier replay required" if ident in priority else "specialist finite/variational route, tied within tier" if ident in finite else "major analytic/theoretical prerequisite, tied within tier","open_claim_leads":[p for p in claims if re.search(r"(?<!\d)"+re.escape(ident.rstrip("a"))+r"(?:a)?(?:\b|:)",p["title"],re.I)]}
  rows.append(row)
 rows.sort(key=lambda r:(r["tier"],r["priority_rank"] or 999,int(re.match(r"\d+",r["id"])[0]),r["id"]))
 report={"research_date_utc":__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),"run_id":os.environ["GITHUB_RUN_ID"],"source_sha":os.environ["GITHUB_SHA"],"upstream_sha":head,"pages":len(rows),"open_prs":len(prs),"ranking_basis":"Analyst practical priority: exact objective, accessible incumbent, structural search headroom, evaluation/certification cost, prior failures. Not empirical success probabilities. Only leading candidates receive full proof/witness audit before experiments; other tiers are preliminary, not claims to have reviewed every cited paper.","rows":rows,"claims":claims}
 (OUT/"ranking.json").write_text(json.dumps(report,indent=2))
 md="# Record-search target ranking\n\nResearch snapshot "+report["research_date_utc"]+". Covers all "+str(len(rows))+" merged constant pages plus open-PR leads. Lower tier/rank is earlier priority. Remaining rows within a tier are tied; numerical ID ordering is for readability, not a fabricated ease distinction. Bounds in the README can be stale, so open claims and actual certificates override them.\n\nTop numerical construction priorities: C3e/C3a (shared masked-alphabet entropy engine), C1b, C1d. C1c is demoted because PR354 reaches the continuum family with piecewise polynomials. C3c/C49a are demoted after this project's negative pilots. Solved rows are excluded. Other specialist rows need a concrete certificate route before any compute allocation.\n\n| Priority | Target | Status |\n|---|---|---|\n"
 for r in rows:md+="|"+(str(r["priority_rank"]) if r["priority_rank"] else "tier"+str(r["tier"])+" (tied)")+"|["+r["id"]+": "+r["name"]+"]("+r["url"]+")|"+r["status"]+"|\n"
 md+="\nRanking is a research allocation judgment, not a guarantee or probability of a record. New unmerged targets (e.g.89b/89c) are not silently counted as existing table constants. All retained bounds must beat the strongest relevant reproduced claim, not just the merged page. See ranking.json for source hashes and open-claim leads.\n"
 (OUT/"RANKING.md").write_text(md)
 print(json.dumps({"pages":len(rows),"top":priority,"upstream_sha":head}))
if __name__=="__main__":main()
