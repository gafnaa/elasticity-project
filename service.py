import sys
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class ServiceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Melakukan komputasi sederhana untuk menaikkan CPU load
        # Sesuaikan angka di dalam range() jika beban CPU kurang terasa atau terlalu berat
        result = 0
        for i in range(100000):
            result += math.sqrt(i)
        
        # Mengirim respon sukses (HTTP 200 OK)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        response_message = f"Request berhasil diproses. (Hasil komputasi: {result})"
        self.wfile.write(response_message.encode('utf-8'))

    # Fungsi ini di-override (ditimpa) untuk menyembunyikan log default HTTP server
    # agar terminal tidak penuh saat load generator mengirimkan banyak request
    def log_message(self, format, *args):
        pass

def run(port):
    server_address = ('localhost', port)
    # Menggunakan ThreadingHTTPServer agar bisa menangani concurrent requests
    httpd = ThreadingHTTPServer(server_address, ServiceHandler)
    
    print(f"Service instance berhasil berjalan di http://localhost:{port}")
    print("Tekan Ctrl+C untuk menghentikan service.")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nMematikan service...")
    finally:
        httpd.server_close()
        print("Service berhenti.")

if __name__ == '__main__':
    # Memastikan pengguna memasukkan argumen port saat menjalankan program
    if len(sys.argv) != 2:
        print("Cara penggunaan: python service.py <port>")
        print("Contoh: python service.py 8001")
        sys.exit(1)
    
    try:
        # Mengambil port dari argumen command line
        port_number = int(sys.argv[1])
        run(port_number)
    except ValueError:
        print("Error: Port harus berupa angka bulat.")
        sys.exit(1)