import json, glob
FIX = {
 "astro-claim-2":   "(-->  high-redshift)",
 "astro-claim-8":   "(-->  bright-transient)",
 "astro-claim-13":  "(-->  hydrogen-fusing)",
 "chem-claim-10":   "(-->  chemically-inert)",
 "mechanics-claim-1": "(-->  accelerates)",
 "mechanics-claim-2": "(-->  momentum-conserved)",
 "mechanics-claim-5":  "(-->  energy-conserved)",
 "mechanics-claim-13": "(-->  significant-drag)",
 "gene-claim-3":    "(-->  produces-mrna)",
 "gene-claim-5":    "(-->  reduced-transcription)",
 "eco-claim-1":     "(-->  trophic-transfer)",
 "eco-claim-3":     "(-->  large-impact-if-removed)",
 "eco-claim-9":     "(-->  breaks-down-organic-matter)",
 "eco-claim-14":    "(-->  growth-limited)",
}
import re
for f in sorted(glob.glob("fixtures/sample_*.jsonl")):
    data = json.load(open(f))
    for c in data["claims"]:
        cid = c["claim_id"]
        if cid in FIX and c.get("metta_atom"):
            a = c["metta_atom"]
            m = re.search(r"\(stv ([\d.]+) ([\d.]+)\)", a)
            stv = m.group(0)
            pred = re.search(r"-->\s+\S+\s+(\S+?)\)?\s*\(\s*$", a.split("==>")[0])
            antecedent = re.search(r"==>\s*\((-->\s+\S+\s+\S+)\)?", a).group(1)
            c["metta_atom"] = "(|- ((==> (%s) (%s)) %s)" % (antecedent.strip("() "), FIX[cid].strip("() "), stv)
    json.dump(data, open(f, "w"), indent=1)
    print(f, "done")
