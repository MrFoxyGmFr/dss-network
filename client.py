import subprocess
import requests
import sys
import uuid
import json
import time

config_file_path = './dss-config.json'
local_config = {}


def set_config(config: dict):
    with open(config_file_path, 'w') as file:
        json.dump(config, file)


def get_config() -> dict:
    try:
        with open(config_file_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError
        config = {"fps": 30, "url": '10.91.89.241', "rtmp_port": 1935, "video_size": (800, 600),
                  "uuid": str(uuid.uuid4()), "last_update": None}

    return config


def edit_config(name, value):
    conf = get_config()
    conf[name] = value
    set_config(conf)
    return conf


CONFIG = get_config()


class Timer:
    class Timer:
        def __init__(self, time, secs, func, replay):
            self.time = time
            self.secs = secs
            self.func = func
            self.replay = replay

        def check(self):
            if time.time() - self.time >= self.secs:
                return (True, self.func(), self.replay, self)
            return (False, None, self.replay)

    def __init__(self):
        self.timers = []

    def check(self):
        _ = []
        for timer_index in range(len(self.timers)):
            ans = self.timers[timer_index].check()
            if ans[0] is True:
                if ans[2] is True:
                    # self.add(ans[3].secs, ans[3].func, ans[3].replay)
                    _.append(self.add(ans[3].secs, ans[3].func, ans[3].replay, ans=True))

            else:
                _.append(self.timers[timer_index])
        self.timers = _.copy()

    def add(self, secs, func, replay: bool = True, ans=False):
        if ans is False:
            self.timers.append(Timer.Timer(time.time(), secs, func, replay))
        else:
            return Timer.Timer(time.time(), secs, func, replay)


class Api:
    def __init__(self, path='/api'):
        self.url_api = 'http://' + CONFIG['url'] + path

    def update(self, uuid):
        global CONFIG
        ans: dict = requests.get(self.url_api + '/config/' + uuid).json()

        return ans


def gen_command_ffmpeg(uuid, video_size=(800, 600), fps=30, url='10.91.89.241', rtmp_port=1935, **kwargs):
    _os = sys.platform
    if _os == 'linux':
        t = 'x11grab'
        monitor = subprocess.run(['echo $DISPLAY'], shell=True, stdout=subprocess.PIPE).stdout.decode().rstrip()
    elif _os == 'win32':
        t = 'gdigrab'
        monitor = 'desktop'
    else:
        raise OSError

    req = "ffmpeg -video_size {w}x{h} -framerate {fps} -f {t} -i {monitor} -c:v libx264 -preset ultrafast -tune zerolatency -f flv 'rtmp://{url}:{rtmp_port}/live/{uuid}'".format(
        w=video_size[0], h=video_size[1], fps=fps, t=t, monitor=monitor, url=url, rtmp_port=rtmp_port, uuid=uuid)

    return req


def start_ffmpeg():
    global CONFIG, local_config
    if local_config['status'] is True:
        print('ffmpeg start')
        _ = local_config.get('ffmpeg_proc', None)
        CONFIG = get_config()
        ffmpeg = gen_command_ffmpeg(**CONFIG)
        _ = subprocess.Popen([ffmpeg], shell=True, stdout=subprocess.PIPE)
        local_config['ffmpeg_proc'] = _
        return _


def stop_ffmpeg():
    print('may_stop')
    _ = local_config.get('ffmpeg_proc', None)
    print(_)
    if _ is not None:
        print(11111)
        try:
            # subprocess.call(['kill '+str(_)], shell=True)
            # print('kill')
            _.terminate()
        except Exception as E:
            print(E)
        # local_config['ffmpeg_proc'] = None


def eval_command(coms: dict):
    global CONFIG, local_config
    print(coms)
    for key, value in coms.items():
        if key == 'setting':
            for key1, value1 in value.items():
                if key1 in CONFIG:
                    CONFIG = edit_config(key1, value1)

            stop_ffmpeg()
            start_ffmpeg()

        elif key == 'status':
            local_config['status'] = value
            if value is True:
                print('start')
                _ = local_config.get('ffmpeg_proc', None)
                if _ is None:
                    print('start 1')
                    stop_ffmpeg()
                    local_config['ffmpeg_proc'] = start_ffmpeg()

            elif value is False:
                stop_ffmpeg()


def get_update(api: Api):
    eval_command(api.update(CONFIG['uuid']))


ffmpeg = gen_command_ffmpeg(**CONFIG)
print(ffmpeg)

api = Api()
timers = Timer()
get_update(api)
timers.add(20, lambda: get_update(api), True)
while True:
    try:
        timers.check()
    except requests.exceptions.ConnectionError:
        pass

# ans = subprocess.Popen([ffmpeg], shell=True, stdout=subprocess.PIPE)
# ans.kill()lll
