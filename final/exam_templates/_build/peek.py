"""print text outputs + errors of executed notebooks (quick sanity check)"""
import json, sys
for f in sys.argv[1:]:
    nb = json.load(open(f))
    print("#" * 20, f)
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        for o in c.get("outputs", []):
            if o["output_type"] == "error":
                print(f"[cell {i}] ERROR {o['ename']}: {o['evalue']}")
            elif o["output_type"] == "stream":
                print(f"[cell {i}]", "".join(o["text"])[:1200])
            elif "text/plain" in o.get("data", {}) and "image/png" not in o["data"]:
                print(f"[cell {i}] ", "".join(o["data"]["text/plain"])[:700])
