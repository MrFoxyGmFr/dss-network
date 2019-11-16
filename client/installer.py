# dss install for linux script use apt install ffmpeg 
# windows vbs in shell:startup dss.py,ffmpeg shell:startup -< 
import os
import sys
import shutil
import ctypes
import getpass
import requests
import subprocess
import urllib.request
from io import BytesIO
from zipfile import ZipFile
import json

service_name = "dss"


if sys.platform.startswith("linux"):
	output = subprocess.check_output("xrandr | grep '*'", shell=True, universal_newlines=True)
	width, height =  output.split()[0].split('x')
elif sys.platform == "win32":
	user32 = ctypes.windll.user32
	width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
url = input('Url of DSS Network server ')
if url.startswith('http://'):
	url = url[7::]
code = getpass.getpass('\033[31mConnection code: \033[0m')
r = requests.post(f"http://{url}/api/connect/{code}", data={'height': height, 'width': width, 'info': os.uname()})
while r.json() == {'error': 'Connection code wrong'}:
	code = getpass.getpass('\033[31mConnection code: \033[0m')
	r = requests.post(f"http://{url}/api/connect/{code}", data={'height': height, 'width': width, 'info': os.uname()})

code = requests.get('https://raw.githubusercontent.com/MrFoxyGmFr/dss-network/dev/client/client.py').text

if sys.platform.startswith("linux"):
	open(f"/usr/sbin/dss-config.json", "w").write(json.dumps(r.json()))
	os.system('apt install -y ffmpeg')
	open(f"/usr/sbin/{service_name}-daemon.py", "w").write(code)
	os.system(f"chmod 777 /usr/sbin/{service_name}-daemon.py")
	open(f"/etc/systemd/system/{service_name}-daemon.service", "w").write(f'[Unit]\nDescription={service_name}\n\n[Service]\nExecStart=/usr/sbin/{service_name}-daemon.py\n\n[Install]\nWantedBy=multi-user.target')
	os.system(f"chmod 664 /etc/systemd/system/{service_name}-daemon.service")
	os.system("systemctl daemon-reload")
	os.system(f"systemctl start {service_name}-daemon")
	os.system(f"systemctl enable {service_name}-daemon")
elif sys.platform == "darwin":
	pass
elif sys.platform == "win32":
	windows_programms = f"C:\\Users\\{os.environ.get('USERNAME')}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\"
	req = urllib.request.Request(
		'https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.2.1-win64-static.zip',
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
		}
	)
	resp = urllib.request.urlopen(req)
	zipfile = ZipFile(BytesIO(resp.read()))
	open(f'{windows_programms}ffmpeg.exe', 'bw').write(zipfile.open('ffmpeg-4.2.1-win64-static/bin/ffmpeg.exe').read())
	py_path = os.path.dirname(sys.executable) + "\\python"
	vbs_script = f"CreateObject(\"Wscript.Shell\").run \"{py_path} \" & Chr(34) & \"{windows_programms}dss.py\" & Chr(34), 0, False"
	open(windows_programms + "dss.py", "w").write(code)
	open(windows_programms + "Startup\\windows.vbs", "w").write(vbs_script)
	open(windows_programms + "dss-config.json", "w").write(json.dumps(r.json()))
	os.system(f"cd {windows_programms}Startup && windows.vbs")
