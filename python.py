import http.server
import json
import socketserver

PORT = 5000


class SandboxHandler(http.server.SimpleHTTPRequestHandler):

  def do_POST(self):
    content_length = int(self.headers.get("Content-Length", 0))
    post_data = self.rfile.read(content_length)

    try:
      # Parsing data JSON yang dikirim dari klien
      data = json.loads(post_data.decode("utf-8"))
      target = data.get("target", "Tidak diketahui")
      method = data.get("method", "Standard")

      # Logika simulasi pemrosesan internal lab
      print(
          f"\n[LAB LOG] Menerima target: {target} | Metode Simulasi:"
          f" {method}"
      )
      response_message = (
          f"Simulasi berhasil diproses untuk target: {target} [ISO-CONTAINED]"
      )

      # Mengirim respons kembali ke klien
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      response_data = {"status": "success", "message": response_message}
      self.wfile.write(json.dumps(response_data).encode("utf-8"))

    except Exception as e:
      self.send_response(400)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      error_data = {"status": "error", "message": str(e)}
      self.wfile.write(json.dumps(error_data).encode("utf-8"))


# Menjalankan server lokal
with socketserver.TCPServer(("", PORT), SandboxHandler) as httpd:
  print(
      f"[NEXORA LAB] Server Python berjalan di http://localhost:{PORT} ..."
  )
  print("[INFO] Gunakan Ctrl+C untuk menghentikan server.")
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    print("\n[NEXORA LAB] Server dihentikan.")