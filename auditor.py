"""Deterministic rule-based text response auditor (not an AI fact checker)."""
import argparse
import json
import re
import sys

def audit(response, rules):
    if not isinstance(response,str) or not isinstance(rules,dict):
        raise ValueError("response must be text and rules an object")
    issues=[]
    minimum=rules.get("min_chars",0)
    maximum=rules.get("max_chars")
    if not isinstance(minimum,int) or isinstance(minimum,bool) or minimum<0:
        raise ValueError("min_chars must be nonnegative integer")
    if maximum is not None and (not isinstance(maximum,int) or isinstance(maximum,bool) or maximum<minimum):
        raise ValueError("max_chars must be integer >= min_chars")
    if len(response)<minimum: issues.append("too_short")
    if maximum is not None and len(response)>maximum: issues.append("too_long")
    for key in ("required_terms","banned_terms"):
        terms=rules.get(key,[])
        if not isinstance(terms,list) or any(not isinstance(x,str) or not x for x in terms):
            raise ValueError(key+" must be an array of nonempty strings")
        for term in terms:
            found=term.casefold() in response.casefold()
            if key=="required_terms" and not found: issues.append("missing:"+term)
            if key=="banned_terms" and found: issues.append("banned:"+term)
    if rules.get("no_urls",False) and re.search(r"https?://\S+",response,re.IGNORECASE):
        issues.append("url_present")
    return {"passed":not issues,"characters":len(response),"issues":issues}

def main(argv=None):
    p=argparse.ArgumentParser(description="Audit text against deterministic rules")
    p.add_argument("file",help="JSON object with response and rules")
    args=p.parse_args(argv)
    try:
        with open(args.file,encoding="utf-8") as f: data=json.load(f)
        if not isinstance(data,dict): raise ValueError("input must be an object")
        result=audit(data.get("response"),data.get("rules",{}))
    except (OSError,ValueError,TypeError) as exc:
        print(str(exc),file=sys.stderr)
        return 2
    print(json.dumps(result,indent=2))
    return 0 if result["passed"] else 1
if __name__=="__main__": raise SystemExit(main())
