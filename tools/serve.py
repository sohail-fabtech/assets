# Local preview server for assets/. The stdlib default queues only 5 connections, which drops images
# when a page requests dozens at once; this raises the backlog. Run: python3 tools/serve.py  → http://localhost:8765/
import functools, http.server, os
http.server.ThreadingHTTPServer.request_queue_size = 256
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
class NoCache(http.server.SimpleHTTPRequestHandler):
    """Preview edits immediately: never let the browser reuse an old SVG/JSON/CSS."""
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


handler = functools.partial(NoCache, directory=root)
http.server.ThreadingHTTPServer(("127.0.0.1", 8765), handler).serve_forever()
