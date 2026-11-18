"""Typed decision: gemma3:1b (Oracle Ollama) picks ONE family from a resume's experience snippet. Schema-constrained, so the answer is always one of FAMS."""
import json, subprocess, re, sys
sys.path.insert(0, 'src')
from fieldclf import FAM
FAMS = [n for n, _ in FAM]
import os
MODEL = os.environ.get('FAM_MODEL', 'gemma3:1b')   # model named by the owner (rule 14); never swap on my own

def snippet(text, n=1400):
    from cvfamily import _lines, START, STOP, SUMMARY
    ex = ' '.join(_lines(text, START, STOP)); sm = ' '.join(_lines(text, SUMMARY, STOP)[:5])
    return re.sub(r'\s+', ' ', (sm[:400] + ' || ' + ex)[:n] if ex else (sm + ' ' + text)[:n])

def ask(text):
    body = {'model': MODEL, 'stream': False, 'options': {'temperature': 0},
            'format': {'type': 'object', 'properties': {'family': {'enum': FAMS + ['none']}}, 'required': ['family']},
            'messages': [{'role': 'user', 'content': 'Fields: ' + ', '.join(FAMS) + '. Read this resume snippet. What field has this person WORKED in (their past roles), not what they study? Answer with one field, or none.\n\n' + snippet(text)}]}
    r = subprocess.run(['ssh', 'oracle', 'curl -s localhost:11434/api/chat -d @-'], input=json.dumps(body), capture_output=True, text=True, timeout=120)
    return json.loads(json.loads(r.stdout)['message']['content'])['family']
