"""Small authenticated AI product: API keys, SQLite user data and usage telemetry."""
import hashlib,json,os,secrets,sqlite3,time,uuid
from datetime import datetime,timezone
from pathlib import Path
from fastapi import FastAPI,HTTPException,Header
from pydantic import BaseModel,Field
DB=Path(os.getenv('DB_PATH',str(Path(__file__).parent/'saas.db')))
app=FastAPI(title='AI SaaS with Evaluation and Monitoring')
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row
 c.execute('CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, email TEXT UNIQUE, password_hash TEXT, token_hash TEXT UNIQUE)')
 c.execute('CREATE TABLE IF NOT EXISTS requests (id TEXT PRIMARY KEY, user_id TEXT, question TEXT, answer TEXT, latency_ms REAL, estimated_input_tokens INTEGER, estimated_output_tokens INTEGER, cost_usd REAL, created_at TEXT)')
 c.commit();return c
class Signup(BaseModel):
 email:str=Field(min_length=5)
 password:str=Field(min_length=12)
class Query(BaseModel):
 question:str=Field(min_length=3,max_length=2000)

def current_user(authorization):
 if not authorization or not authorization.startswith('Bearer '):raise HTTPException(401,'Bearer token required')
 token=authorization.removeprefix('Bearer ').strip()
 digest=hashlib.sha256(token.encode()).hexdigest()
 c=connect();user=c.execute('SELECT * FROM users WHERE token_hash=?',(digest,)).fetchone();c.close()
 if not user:raise HTTPException(401,'Invalid token')
 return dict(user)
@app.post('/signup',status_code=201)
def signup(body:Signup):
 token=secrets.token_urlsafe(32);id=str(uuid.uuid4())
 salt=secrets.token_bytes(16)
 hashed=salt.hex()+':'+hashlib.scrypt(body.password.encode(),salt=salt,n=2**14,r=8,p=1).hex()
 c=connect()
 try:
  with c:c.execute('INSERT INTO users VALUES (?,?,?,?)',(id,body.email.lower(),hashed,hashlib.sha256(token.encode()).hexdigest()))
 except sqlite3.IntegrityError:raise HTTPException(409,'Email already registered')
 finally:c.close()
 return {'user_id':id,'api_token':token,'warning':'Token shown once. Store securely.'}

def ai_answer(question):
 if not os.getenv('OPENAI_API_KEY'):
  return 'Demo mode: AI provider not configured. Input received: '+question[:120],0,0,'mock'
 response=__import__('openai').OpenAI().chat.completions.create(model=os.getenv('OPENAI_MODEL','gpt-4o-mini'),messages=[{'role':'system','content':'You are an enterprise workflow advisor. Be accurate, concise, and state uncertainty.'},{'role':'user','content':question}])
 u=response.usage
 return response.choices[0].message.content or '',u.prompt_tokens if u else 0,u.completion_tokens if u else 0,'openai'
@app.post('/ai/query')
def query(body:Query,authorization:str|None=Header(None)):
 user=current_user(authorization);t=time.perf_counter()
 try:answer,input_t,output_t,provider=ai_answer(body.question)
 except Exception:raise HTTPException(502,'Upstream model error')
 latency=(time.perf_counter()-t)*1000
 # Configure provider token prices yourself; defaults zero to avoid invented billing rates.
 in_rate=float(os.getenv('INPUT_USD_PER_1M','0'));out_rate=float(os.getenv('OUTPUT_USD_PER_1M','0'))
 cost=(input_t*in_rate+output_t*out_rate)/1e6
 id=str(uuid.uuid4());c=connect()
 with c:c.execute('INSERT INTO requests VALUES (?,?,?,?,?,?,?,?,?)',(id,user['id'],body.question,answer,round(latency,2),input_t,output_t,round(cost,8),datetime.now(timezone.utc).isoformat()))
 c.close();return {'request_id':id,'answer':answer,'provider':provider,'latency_ms':round(latency,2),'input_tokens':input_t,'output_tokens':output_t,'estimated_cost_usd':round(cost,8),'cost_rates_configured':bool(in_rate or out_rate)}
@app.get('/metrics')
def metrics(authorization:str|None=Header(None)):
 user=current_user(authorization);c=connect();rows=c.execute('SELECT latency_ms,cost_usd FROM requests WHERE user_id=? ORDER BY latency_ms',(user['id'],)).fetchall();c.close()
 n=len(rows);times=[r['latency_ms'] for r in rows]
 return {'requests':n,'p50_latency_ms':times[int((n-1)*.5)] if n else None,'p95_latency_ms':times[int((n-1)*.95)] if n else None,'estimated_total_cost_usd':round(sum(r['cost_usd'] for r in rows),7),'note':'Cost 0 means no model usage or missing configured rates.'}
@app.get('/health')
def health():return {'status':'ok'}

from fastapi.responses import FileResponse
@app.get("/")
def homepage():return FileResponse(Path(__file__).parent/"frontend"/"index.html")
