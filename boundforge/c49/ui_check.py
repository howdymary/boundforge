"""Remote Playwright check of the actual offline artifact, including witness download."""
import json,pathlib
from playwright.sync_api import sync_playwright
HERE=pathlib.Path(__file__).resolve().parent
def check():
 out=HERE/"ui-checks";out.mkdir(exist_ok=True);report={"screens":[],"scope":"Actual offline artifact, Chromium desktop/mobile and downloaded finite witness; browser is not the exact mathematical verifier."}
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for width in [1440,390]:
   page=browser.new_page(viewport={"width":width,"height":1000},device_scale_factor=1);errors=[];page.on("pageerror",lambda e:errors.append(str(e)))
   page.goto((HERE/"results/demo.html").as_uri());page.wait_for_selector("#trace tr")
   assert page.locator("#trace tr").count()==24
   assert page.evaluate("document.documentElement.scrollWidth<=window.innerWidth"),("horizontal overflow",width)
   before=page.locator("#episode").text_content();page.locator("#arm").select_option("scheduled");assert page.locator("#episode").text_content()!=before
   page.locator("#arm").select_option("full");page.locator("#seed").select_option("410")
   with page.expect_download() as dl:page.locator("#download").click()
   obj=json.loads(pathlib.Path(dl.value.path()).read_text());source=json.loads((HERE/"results/evaluation/episodes/uniform9/full.json").read_text())
   row=next(r for r in source if r["seed"]==410)
   assert obj["masks"]==row["best_family"] and obj["ports"]==row["ports"]
   page.screenshot(path=str(out/("desktop.png" if width==1440 else "mobile.png")),full_page=True)
   assert not errors,errors
   report["screens"].append({"width":width,"page_errors":errors,"horizontal_overflow":False,"trace_rows":24,"download_matches_recorded_witness":True})
   page.close()
  browser.close()
 (out/"report.json").write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=="__main__":check()
