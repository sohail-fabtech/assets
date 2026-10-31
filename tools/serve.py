# Local preview server for assets/. The stdlib default queues only 5 connections, which drops images
# when a page requests dozens at once; this raises the backlog. Run: python3 tools/serve.py  → http://localhost:8765/
import functools, http.server, os
http.server.ThreadingHTTPServer.request_queue_size = 256
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
http.server.ThreadingHTTPServer(("127.0.0.1", 8765), handler).serve_forever()
