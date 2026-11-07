#!/usr/bin/env python3
"""Local server: serves this folder and saves notes to my-notes.json beside each notes.html.
Run:  python3 serve.py   then open http://localhost:8000/"""
import http.server, os, urllib.parse
ROOT=os.path.dirname(os.path.abspath(__file__))
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=ROOT,**k)
    def do_POST(s):
        u=urllib.parse.urlparse(s.path)
        if u.path!='/__save': s.send_error(404); return
        p=urllib.parse.unquote(urllib.parse.parse_qs(u.query).get('p',[''])[0]).lstrip('/')
        d=os.path.normpath(os.path.join(ROOT,os.path.dirname(p)))
        if not p.endswith('notes.html') or not d.startswith(ROOT): s.send_error(400); return
        body=s.rfile.read(int(s.headers.get('Content-Length',0)))
        with open(os.path.join(d,'my-notes.json'),'wb') as f: f.write(body)
        s.send_response(200); s.end_headers(); s.wfile.write(b'ok')
http.server.test(HandlerClass=H,port=8000,bind='127.0.0.1')
