#Kode ini membuat koneksi Modbus TCP, terus-menerus membaca nilai dari register 0, 
#dan menampilkan hasilnya secara real-time tanpa berpindah baris.

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import time

# Konfigurasi koneksi Modbus
SERVER_IP = '192.168.1.177' # IP ARDUINO
SERVER_PORT = 502


# Konfigurasi membaca holding_register (40001)
def read_holding_register(client, address):
    try:
        result = client.read_holding_registers(address=address, count=1)
        if not result.isError():
            return result.registers[0]
        else:
            return None
    except (ModbusException, Exception):
        return None

# Konfigurasi menghubungkan ke server Modbus (membaca alamat nilai register 0 setiap detik)
def main():
    client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)
    
    try:
        if client.connect():
            print(f"Berhasil terhubung ke {SERVER_IP}:{SERVER_PORT}")
            print("Nilai Register 0: ", end='', flush=True)
            
            while True:
                register_value = read_holding_register(client, address=0)
                
                if register_value is not None:
                    print(f"\rNilai Register 0: {register_value}", end='', flush=True)
                else:
                    print("\rGagal membaca register", end='', flush=True)
                
                time.sleep(1)
        else:
            print("Gagal terhubung ke server Modbus")
    
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna")
    
    finally:
        client.close()
        print("\nKoneksi Modbus ditutup")

if __name__ == "__main__":
    main()
