import time
import psutil
import requests

INFLUXDB_URL = 'http://localhost:8086/write?db=metrics'
HOSTNAME = 'localmachine'  

def send_metric(measurement, fields):
    line = f"{measurement},host={HOSTNAME} " + ",".join([f"{k}={v}" for k, v in fields.items()])
    try:
        requests.post(INFLUXDB_URL, data=line, auth=('admin', 'admin123'))
    except Exception as e:
        print("Error sending data to InfluxDB:", e)

while True:
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent 
    net = psutil.net_io_counters()
    net_bytes_sent = net.bytes_sent
    net_bytes_recv = net.bytes_recv

    send_metric('system_metrics', {
        'cpu': cpu,
        'memory': memory,
        'disk': disk,
        'net_sent': net_bytes_sent,
        'net_recv': net_bytes_recv
    })

    print(f"Sent metrics - CPU: {cpu}%, Mem: {memory}%, Disk: {disk}%")
    time.sleep(10)  
