"""Deterministic regression rubric for configured LLM answers; not a fact-checker."""
import os,json,httpx
QUESTIONS=[('What should an AI procurement policy include?', ['risk','data']),('Summarize why audit logs matter.', ['audit'])]
def main():
 base=os.getenv('BASE_URL','http://127.0.0.1:8000');c=httpx.Client(base_url=base,timeout=60)
 from uuid import uuid4
 token=c.post('/signup',json={'email':f'eval-{uuid4()}@example.test','password':'local-demo-password-123'}).json()['api_token']
 headers={'Authorization':'Bearer '+token}
 rows=[]
 for q,keywords in QUESTIONS:
  r=c.post('/ai/query',json={'question':q},headers=headers);r.raise_for_status();answer=r.json()['answer'].lower()
  rows.append({'question':q,'keyword_coverage':sum(k in answer for k in keywords)/len(keywords)})
 print(json.dumps({'results':rows,'metric':'weak lexical regression proxy; needs human rubric','telemetry':c.get('/metrics',headers=headers).json()},indent=2))
if __name__=='__main__':main()
