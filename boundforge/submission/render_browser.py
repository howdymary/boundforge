"""Remote headless smoke/visual QA of the generated offline viewer."""
import json,pathlib,re,shutil,subprocess
HERE=pathlib.Path(__file__).resolve().parent;D=HERE/"demo";url=(D/"index.html").resolve().as_uri()
chrome=shutil.which("google-chrome")or shutil.which("chromium")
if not chrome:raise RuntimeError("headless Chrome unavailable")
base=[chrome,"--headless=new","--no-sandbox","--disable-gpu","--disable-background-networking","--disable-sync","--no-first-run","--no-default-browser-check","--host-resolver-rules=MAP * ~NOTFOUND","--virtual-time-budget=1500"]
p=subprocess.run(base+["--dump-dom",url],capture_output=True,text=True,timeout=45)
if p.returncode or not re.search(r'id="runtime">[0-9.]+ seconds',p.stdout):raise ValueError("viewer initialization failed")
if "SyntaxError" in p.stderr:raise ValueError("viewer JavaScript syntax error")
for size,name in [("1440,1400","viewer-desktop.png"),("390,1400","viewer-mobile.png")]:
 subprocess.run(base+["--window-size="+size,"--screenshot="+str((D/name).resolve()),url],capture_output=True,check=True,timeout=45)
(D/"browser-qa.json").write_text(json.dumps({"initialized":True,"desktop":"1440x1400","mobile":"390x1400","scope":"Remote headless rendering, not manipulation of the user's browser or a deployed site."},indent=2))
