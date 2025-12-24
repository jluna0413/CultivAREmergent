import json, sys, re
files=[r".cursor/mcp.json", r"ops/ollama-gemma1b/mcp_snippet.json", r".vscode/settings.json"]
base=r"a:\\dev\\CultivAREmergant\\"

def strip_jsonc(s):
    # remove // comments and /* */ comments
    s=re.sub(r"//.*?\n", "\n", s)
    s=re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return s

for f in files:
    path=base+f.replace('/','\\\\')
    print('==',f,'==')
    try:
        with open(path,'r',encoding='utf-8') as fh:
            raw=fh.read()
        # try strict parse first
        try:
            json.loads(raw)
            print('OK: strict JSON parse succeeded')
        except Exception as e:
            print('STRICT JSON parse FAILED:', e)
            # try JSONC stripping
            try:
                cleaned=strip_jsonc(raw)
                json.loads(cleaned)
                print('After stripping comments: JSON parse succeeded (file is JSONC)')
            except Exception as e2:
                print('After stripping comments: parse FAILED:', e2)
    except FileNotFoundError:
        print('File not found:',path)
    print()
