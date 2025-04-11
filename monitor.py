import time
import psutil
import requests


INFLUXDB_URL = 'http://127.0.0.1:8086/write?db=metrics'  # Changed to direct localhost IP
HOSTNAME = 'localmachine'
AUTH = ('admin', 'admin123')  

def send_metric(measurement, fields):
  
    fields_str = ",".join([f"{k}={v}" for k, v in fields.items()])
    line = f"{measurement},host={HOSTNAME} {fields_str}"
    
    try:
        response = requests.post(
            INFLUXDB_URL,
            data=line,
            auth=AUTH,
            headers={'Content-Type': 'application/octet-stream'},
            timeout=5
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending data to InfluxDB: {e}")

if __name__ == "__main__":
    while True:
        # Collect metrics
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net = psutil.net_io_counters()
        
        # Send metrics
        send_metric('system_metrics', {
            'cpu': float(cpu),
            'memory': float(memory),
            'disk': float(disk),
            'net_sent': int(net.bytes_sent),
            'net_recv': int(net.bytes_recv)
        })

        print(f"Sent metrics - CPU: {cpu}%, Mem: {memory}%, Disk: {disk}%")
        time.sleep(10)
