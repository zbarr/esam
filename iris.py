import eventlet
eventlet.sleep()
eventlet.monkey_patch()

import json
import csv
from threading import Thread, Event
from queue import Queue
from math import floor
import datetime
import time

from appdict import ApplicationDict, CronDict, Application
from log_base import LogBase

import eventlet.green.zmq as zmq
import requests
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import pytz


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, logger=True, engineio_logger=True)
log_date = datetime.datetime.now()
# log = LogBase('log/iris.' + str(log_date.year) + str(log_date.month) + str(log_date.day) + '.log')
log = LogBase('log/iris.' + log_date.strftime("%Y%m%d"))
clients = []
rogue = False

# ------------------------- #
# ----- Static Routes ----- #
# ------------------------- #

@app.route('/')
@app.route('/home')
def home_view():
    log.logger.info("Serving home_view to " + request.remote_addr)
    home_list = master_app_dict.home_list

    collapse = request.args.get('collapse', "true")


    if request.args.get('view') == "true":
        template = "datacenter_view.html"
        simple_desk_list = []
    else:
        simple_desk_list = master_app_dict.simple_desk_list
        template = "layout.html"

    home_view = render_template(template, data = home_list, type = "home", desk_list = sorted(simple_desk_list))
    return home_view



@app.route('/suites')
def suite_view():
    log.logger.info("Serving suite_view to " + request.remote_addr)
    suite_list = master_app_dict.suite_list

    if request.args.get('view') == "true":
        template = "datacenter_view.html"
        simple_desk_list = []
    else:
        simple_desk_list = master_app_dict.simple_desk_list
        template = "layout.html"

    suite_view = render_template(template, data = suite_list, type = "suites", desk_list = sorted(simple_desk_list))
    return suite_view


@app.route('/datacenters')
def datacenter_view():
    log.logger.info("Serving datacenter_view to " + request.remote_addr)
    datacenter_list = master_app_dict.datacenter_list

    if request.args.get('view') == "true":
        template = "datacenter_view.html"
        simple_desk_list = []
    else:
        simple_desk_list = master_app_dict.simple_desk_list
        template = "layout.html"

    datacenter_view = render_template(template, data = datacenter_list, type = "datacenters", desk_list = sorted(simple_desk_list))
    return datacenter_view

@app.route('/desks')
@app.route('/desks/<desk>')
def desk_view(desk = None):
    log.logger.info("Serving desk_view to " + request.remote_addr)
    desks = master_app_dict.desks
    desk_list = master_app_dict.desk_list

    # desk = request.args.get('desk')
    if desk:
        data = [[desk, desks[desk]]]
    else:
        data = desk_list

    if request.args.get('view') == "true":
        template = "datacenter_view.html"
        simple_desk_list = []
    else:
        simple_desk_list = master_app_dict.simple_desk_list
        template = "layout.html"

    desk_view = render_template(template, data = data, type = "desks", desk_list = sorted(simple_desk_list))

    return desk_view


@app.route('/monitor')
def monitor_view():
    log.logger.info("Serving monitor_view to " + request.remote_addr)
    home_list = master_app_dict.home_list

    if request.args.get('view') == "true":
        template = "datacenter_view.html"
        simple_desk_list = []
    else:
        simple_desk_list = master_app_dict.simple_desk_list
        template = "layout.html"

    home_view = render_template(template, data = home_list, type = "monitor", desk_list = sorted(simple_desk_list))
    return home_view

@app.route('/hosts-sapphire')
def hosts_sapphire_json():
    log.logger.info("Serving Sapphire hosts to " + request.remote_addr)
    suites = master_app_dict.suites
    output_list = []
    for app in suites["sapphire"]:
        output_list.append(app["host"])
    return json.dumps(output_list)


# ------------------------------ #
# ----- Websocket Handlers ----- #
# ------------------------------ #

@socketio.on('connect')
def connect_log():
    log.logger.info("Client connected: " + request.remote_addr)
    clients.append(request.remote_addr)

@socketio.on_error()
def error_handler(e):
    log.logger.error(e)

@socketio.on('disconnect')
def disconnect_log():
    log.logger.info("Client disconnected: " + request.remote_addr)
    clients.remove(request.remote_addr)


# ------------------------ #
# ----- Initializers ----- #
# ------------------------ #

def refresh_data(applications, cron_dict):

    # ----- Clear other data ----- #
    applications.clear()
    cron_dict.clear()

    # Get salt json and convert to dict
    salt_json = requests.get("http://skip/salt-pillars.json").text
    salt_data = json.loads(salt_json)

    for host in salt_data:

        if "applications" in salt_data[host]:
            # used_apps = ["linux_script", "windows_script", "marketbook-viewer", "lens", "downloader", "ccs2-downloader"]
            # used_apps = ["marketbook-viewer", "lens"]
            app_list = salt_data[host]["applications"]
            used_apps = ["linux_script", "windows_script", "marketbook-viewer", "lens", "cadmin"]

            for app in app_list:
                app_suite = app.split("-")[0].lower()
                dashes = 1

                while app_suite not in salt_data[host]:
                    dashes += 1
                    app_suite = "-".join(app.split("-")[0:dashes]).lower()

                if app_suite not in used_apps:
                    used_apps.append(app_suite)

                    for instance in salt_data[host][app_suite]:
                        if app_suite == "tsdb":
                            name = salt_data[host][app_suite][instance]["exchange"]
                        else:
                            name = instance

                        app_dict = Application(host.lower(), app_suite, name)

                        if salt_data[host].get("datacenter"):
                            datacenter = salt_data[host].get("datacenter")
                            if datacenter == "qa1":
                                break;
                            else:
                                app_dict.datacenter = datacenter

                        else:
                            datacenter = app_dict.datacenter

                        app_key = (app_dict.host.split('.')[0] + "-" + app_dict.suite + "-" + app_dict.name).lower()

                        # ----- Timezone support ----- #
                        if "new_york" in datacenter:
                            tz = pytz.timezone('America/New_York')
                        elif "tokyo" in datacenter:
                            tz = pytz.timezone('Japan')
                        else:
                            tz = None

                        # ----- Setting initial cron status ----- #
                        if  salt_data[host][app_suite][instance].get("cron_enabled"):
                            app_dict.cron = salt_data[host][app_suite][instance]["cron"]
                            app_dict.cron_list = get_cron_list(app_dict.cron, app_key, tz, cron_dict)

                            datetime_weekday = (datetime.datetime.now().weekday() + 1) % 7

                            if app_dict.cron_list.get(datetime_weekday):
                                for cron_index, cron_object in enumerate(app_dict.cron_list[datetime_weekday]):
                                    if datetime.datetime.time(datetime.datetime.now()).replace(second=0, microsecond=0) < cron_object["time"]:
                                        if cron_index != 0:
                                            app_dict.cron_status = app_dict.cron_list[datetime_weekday][cron_index - 1]["status"]
                                            break;

                                        else:
                                            app_dict.cron_status = get_last_cron_status(app_dict.cron_list, datetime_weekday)
                                            break;

                                    elif cron_index == len(app_dict.cron_list[datetime_weekday]) - 1:
                                        app_dict.cron_status = app_dict.cron_list[datetime_weekday][cron_index]["status"]


                            elif app_dict.cron_list:
                                app_dict.cron_status = get_last_cron_status(app_dict.cron_list, datetime_weekday)


                        # ----- Getting desk ----- #
                        if "acc_desk" in salt_data[host][app_suite][instance]:
                            app_dict.desk = salt_data[host][app_suite][instance]["acc_desk"]
                        elif "desk" in salt_data[host][app_suite][instance]:
                            app_dict.desk = salt_data[host][app_suite][instance]["desk"]

                        # ----- Mapping house and all desk to ssvcs ----- #
                        if app_dict.desk in ["house", "all"]:
                            app_dict.desk = "ssvcs"

                        applications.add_app(app_key, app_dict)


def get_beating_apps(applications):

    # Socket to talk to server
    min_words = 2
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://e7heartbeat:5589")

    zmqfilter = u""
    socket.setsockopt_string(zmq.SUBSCRIBE, zmqfilter)
    inbound_data = socket.recv_string().lower()

    for line in inbound_data.splitlines():
        words = line.replace("timeseriesdbservice","tsdb").split()
        if len(words) > 2:
            log.logger.error("Snapshot heartbeat string has too many words delimited by whitespace: " + ' '.join(words))
        else:
            word_list = (words[0].split('.')[0] + '-' + words[1]).split('-')
            original_word_list = word_list.copy()

            if word_list[-1] in ["log_reader", "controller"]:
                if word_list[-1] == "log_reader":
                    status_type = "lr_status"
                else:
                    status_type = "hb_status"
                word_list.pop()
            else:
                status_type = "hb_status"

            if len(word_list) == min_words:
                log.logger.error("No suite in snapshot heartbeat string: " + '-'.join(word_list))
                if rogue:
                    log.logger.info("Adding rogue app anyway...")
                    new_app = Application(word_list[0], "rogue", word_list[1], "rogue", "rogue", "up")
                    applications.add_app('-'.join(word_list), new_app)
            else:
                for index in range(min_words, len(word_list)):

                    test_word_list = word_list[0:index]
                    test_word_list.append(str(word_list[-1]))
                    test_string = '-'.join(test_word_list)

                    if test_string in applications.get_apps():
                        applications.get_app(test_string).update_status(status_type, "up")
                        break;
                else:
                    log.logger.error("Non-matching snapshot heartbeat string: %s" % test_string)
                    if rogue:
                        log.logger.info("Adding rogue app anyway...")
                        new_app = Application(word_list[0], "rogue", '-'.join(original_word_list[1:]), "rogue", "rogue", "up")
                        applications.add_app('-'.join(original_word_list), new_app)

    socket.disconnect("tcp://e7heartbeat:5589")
    socket.close()
    context.term()


# --------------------------------------- #
# ----- Cron Logic Helper Functions ----- #
# --------------------------------------- #

def current_dayweek():
    return (datetime.datetime.now().weekday() + 1) % 7

def current_hour_minute():
    return datetime.datetime.time(datetime.datetime.now()).replace(second=0, microsecond=0)

def get_cron_list(crons, key, zone, cron_dict):
    cron_list = {}

    # ----- Checking if we have both start and stop crons ----- #
    start_bool = False
    stop_bool = False
    for cron_type, cron_info in crons.items():
        if "start" in cron_type:
            start_bool = True
        elif "stop" in cron_type:
            stop_bool = True
        else:
            log.logger.warning("Bad cron_type: " + cron_type)

    # ----- Creating new cron data structures ----- #
    if start_bool and stop_bool:
        for cron_type, cron_info in crons.items():
            dayweek_string = cron_info["dayweek"]
            hour = int(cron_info["hour"])
            minute = int(cron_info["minute"])
            delta = datetime.datetime.now(tz=None).hour - datetime.datetime.now(tz=zone).hour
            hour_adjusted = (hour + delta) % 24
            dayweek_adjustment = floor((hour + delta)/24)

            cron_time = datetime.time(hour_adjusted, minute)

            if "start" in cron_type:
                type = "up"
            elif "stop" in cron_type:
                type = "down"
            else:
                log.logger.warning("Bad cron_type: " + value["cron"])
                type = "ERROR"

            if "-" not in dayweek_string:
                dayweek_adjusted = (int(dayweek_string) + dayweek_adjustment) % 7

                # ----- Adding cron to app: {1:[{"status": "time": }, ...], ...} ----- #
                cron_list[dayweek_adjusted] = set_crons(cron_list.get(dayweek_adjusted, []), cron_time, type)

                # ----- Adding cron to global: {1:{time: [{app: status:}, ...], ...}, ...} ----- #
                cron_dict.add_entry(dayweek_adjusted, cron_time, key, type)

            else:
                for dayweek_index in range(int(dayweek_string.split('-')[0]), int(dayweek_string.split('-')[1]) + 1):
                    dayweek_adjusted = (dayweek_index + dayweek_adjustment) % 7

                    # ----- Adding cron to app: {1:[{"status": "time": }, ...], ...} ----- #
                    cron_list[dayweek_adjusted] = set_crons(cron_list.get(dayweek_adjusted, []), cron_time, type)

                    # ----- Adding cron to global: {1:{time: [{app: key:}, ...], ...}, ...} ----- #
                    cron_dict.add_entry(dayweek_adjusted, cron_time, key, type)

    else:
        cron_list = {}

    return cron_list

def set_crons(day_list, day_time, type):
    if not day_list:
        day_list.append({"status": type, "time": day_time})
    else:
        for time_index, time_value in enumerate(day_list):

            if time_value["time"] > day_time:
                day_list.insert(time_index, {"status": type, "time": day_time})
                break;
            elif time_index == (len(day_list) - 1):
                day_list.append({"status": type, "time": day_time})
                break;
    return day_list

def get_last_cron_status(cron_object, weekday):

    for index in range(weekday - 1, -1, -1):
        if index in cron_object:
            return cron_object[index][-1]["status"]

    for index in range(6, weekday, -1):
        if index in cron_object:
            return cron_object[index][-1]["status"]

    log.logger.warning("No crons were found when getting last cron status")
    return "ERROR"

def make_wincrons(applications, cron_dict):
    modified_app_list = []
    filename = "crons.txt"
    with open(filename) as inputfile:
        for raw_line in inputfile:

            min_words = 2
            raw_line = raw_line.lower().replace("timeseriesdbservice", "tsdb")
            line = raw_line.split()
            dayweek = line[4]
            hour = line[1]
            minute = line[0]
            if '#' not in minute:
                for index, section in enumerate(line):
                    if "llc" in section:
                        app_string_section = section
                        if "start" in section.lower():
                            type = "start_" + dayweek + "_" + minute
                        elif "stop" in section.lower():
                            type = "stop_" + dayweek + "_" + minute
                        else:
                            log.logger.warning("No cron_type: " + section)
                            type = "ERROR"
                        break;
                else:
                    type = "ERROR"
                    log.logger.warning("No cron type in wincron: %s" % line)


                app_string = app_string_section.split("\\")[1]
                if app_string == "service-control":
                    app_string = line[index + 2].replace("\"", "").replace("\'", "")

                word_list = (line[8].replace("\'","").split('.')[0] + "-" + app_string).lower().split('-')

                if len(word_list) == min_words:
                    log.logger.warning("No app suite in wincron string: " + '-'.join(word_list))
                else:
                    for index in range(min_words, len(word_list)):

                        test_word_list = word_list[0:index]
                        test_word_list.append(str(word_list[-1]))
                        test_string = '-'.join(test_word_list)

                        if test_string in applications.get_apps():


                            applications.get_app(test_string).set_cron(type, dayweek, minute, hour)
                            if test_string not in modified_app_list:
                                modified_app_list.append(test_string)
                            break;

                    else:
                        log.logger.warning("Non-matching wincron string: %s" % test_string)

        inputfile.close()

    for app in modified_app_list:
        current_app = applications.get_app(app)
        current_app.cron_list = get_cron_list(current_app.cron, app, None, cron_dict)

        datetime_weekday = (datetime.datetime.now().weekday() + 1) % 7

        if current_app.cron_list.get(datetime_weekday):
            for cron_index, cron_object in enumerate(current_app.cron_list[datetime_weekday]):
                if datetime.datetime.time(datetime.datetime.now()).replace(second=0, microsecond=0) < cron_object["time"]:
                    if cron_index != 0:
                        current_app.cron_status = current_app.cron_list[datetime_weekday][cron_index - 1]["status"]
                        break;

                    else:
                        current_app.cron_status = get_last_cron_status(current_app.cron_list, datetime_weekday)
                        break;

                elif cron_index == len(current_app.cron_list[datetime_weekday]) - 1:
                    current_app.cron_status = current_app.cron_list[datetime_weekday][cron_index]["status"]


        elif current_app.cron_list:
            current_app.cron_status = get_last_cron_status(current_app.cron_list, datetime_weekday)

# ------------------- #
# ----- Threads ----- #
# ------------------- #

def heartbeat_recv(q, event):
    log.logger.info("Starting heartbeat_recv...")

    status_map = {"logon:":"up", "warning:":"none", "critical:":"none", "logoff:":"down"}
    alert_map = {"logon:":"none", "warning:":"warning","critical:":"critical", "logoff:":"none"}
    min_words = 2

    heartbeat_context = zmq.Context()
    heartbeat_socket = heartbeat_context.socket(zmq.SUB)
    heartbeat_socket.connect("tcp://e7heartbeat:5556")
    filter = u""
    heartbeat_socket.setsockopt_string(zmq.SUBSCRIBE, filter)
    # socketio.sleep(5)
    while True:
        msg = heartbeat_socket.recv_string().lower().replace("timeseriesdbservice","tsdb").split()

        status = status_map[msg[2]]
        alert = alert_map[msg[2]]
        word_list = (msg[4].split('.')[0] + "-" + msg[5]).split('-')

        if word_list[-1] in ["log_reader", "controller"]:
            if word_list[-1] == "log_reader":
                status_type = "lr_status"
            else:
                status_type = "hb_status"
            word_list.pop()
        else:
            status_type = "hb_status"

        if alert != "none":
            status_type = "alert"

        status_object = {"app_name":word_list, "type":status_type, "status":status, "alert":alert}
        log.logger.info("Putting incremental heartbeat update in queue: " + json.dumps(status_object))
        q.put(status_object)
        event.set()

def state_updater(q, event, applications, cron_dict):
    log.logger.info("Starting state_updater...")

    while True:
        event.wait()
        while not q.empty():
            update = q.get()
            log.logger.info("Got update from queue: " + json.dumps(update))

            if update["type"] == "reset":
                refresh_data(applications, cron_dict)
                make_wincrons(applications, cron_dict)
                get_beating_apps(applications)
                applications.init_templates()
                log.logger.info("Sending reset signal to clients: " + str(clients))
                socketio.emit('reset')

            else:
                min_words = 2
                word_list = update['app_name']
                if len(word_list) == min_words:
                    log.logger.error("No suite in update: " + '-'.join(word_list))
                    if rogue:
                        if update["status"] == "up":
                            log.logger.info("Adding rogue app anyway...")
                            new_app = Application(word_list[0], "rogue", word_list[1], "rogue", "rogue", "up")
                            applications.add_app('-'.join(word_list), new_app)
                            socketio.emit('reset')
                            log.logger.info("Sent reset to clients for rogue app: " + str(clients) + "\n" + json.dumps(new_app))
                        elif update["status"] == "down":
                            log.logger.info("Removing rogue app anyway...")
                            if applications.remove_app('-'.join(word_list)):
                                socketio.emit('reset')
                                log.logger.info("Sent reset to clients for rogue app shutdown: " + str(clients) + "\n" + '-'.join(word_list))
                            else:
                                log.logger.error("Trying to shut down an app that is not up: " + '-'.join(word_list))
                        else:
                            log.logger.info("Alerting on rogue app...")
                            if update["alert"] == "warning":
                                color = "#f4ee42"
                            else:
                                color = "#f44141"
                            update['color'] = color
                            update['app_name'] = word_list[0] + '-rogue-' + word_list[1]
                            socketio.emit('update', {'data': update})
                            log.logger.info("Sent update to clients: " + str(clients) + "\n" + json.dumps(update))
                else:
                    for index in range(min_words, len(word_list)):


                            test_word_list = word_list[0:index]
                            test_word_list.append(str(word_list[-1]))
                            test_string = '-'.join(test_word_list)

                            if test_string in applications.get_apps():

                                if update["type"] == "alert":
                                    if update["alert"] == "warning":
                                        color = "#f4ee42"
                                    else:
                                        color = "#f44141"
                                else:
                                    color = applications.update_app_status(test_string, update["type"], update["status"])

                                update['color'] = color
                                update['app_name'] = test_string
                                socketio.emit('update', {'data': update})
                                log.logger.info("Sent update to clients: " + str(clients) + "\n" + json.dumps(update))
                                break;

                    else:
                        log.logger.error("Non-matching heartbeat string: %s" % update['app_name'])
                        if rogue:
                            if update["status"] == "up":
                                log.logger.info("Adding rogue app anyway...")
                                new_app = Application(word_list[0], "rogue", word_list[1], "rogue", "rogue", "up")
                                applications.add_app('-'.join(word_list), new_app)
                                socketio.emit('reset')
                                log.logger.info("Sent reset to clients for rogue app: " + str(clients) + "\n" + json.dumps(new_app))
                            elif update["status"] == "down":
                                log.logger.info("Removing rogue app anyway...")
                                if applications.remove_app('-'.join(word_list)):
                                    socketio.emit('reset')
                                    log.logger.info("Sent reset to clients for rogue app: " + str(clients) + "\n" + '-'.join(word_list))
                                else:
                                    log.logger.error("Trying to shut down an app that is not up: " + '-'.join(word_list))
                            else:
                                log.logger.info("Alerting on rogue app...")
                                if update["alert"] == "warning":
                                    color = "#f4ee42"
                                else:
                                    color = "#f44141"
                                update['color'] = color
                                update['app_name'] = word_list[0] + '-rogue-' + word_list[1]
                                socketio.emit('update', {'data': update})
                                log.logger.info("Sent update to clients: " + str(clients) + "\n" + json.dumps(update))



        event.clear()

def cron_watcher(q, event, cron_dict):
    log.logger.info("Starting cron_watcher...")
    starttime = time.time() - (time.time() % 60)
    while True:
        # print(cron_dict.get_apps(2, datetime.datetime.time(datetime.datetime.now()).replace(hour=2, minute=55, second=0, microsecond=0)))
        # ----- Check for salt updates ----- #
        if datetime.datetime.now().minute % 5 == 0:
            log.logger.info("Sending reset trigger to updater - sleeping for another 5 minutes")
            status_object = {"app_name": None, "type": "reset", "status": None, "alert": None}
            q.put(status_object)
            event.set()
        dayweek = current_dayweek()
        hour_minute = current_hour_minute()
        if cron_dict.check_time(dayweek, hour_minute):
            for app in cron_dict.get_apps(dayweek, hour_minute):
                status_object = {"app_name": app["app"].split('-'), "type": "cron_status", "status": app["status"], "alert": "none"}
                log.logger.info("Putting status_object from cron_watcher in queue: " + json.dumps(status_object))
                q.put(status_object)

            event.set()

        log.logger.info("Updated cron schedules - sleeping for another minute")
        time.sleep(60.0 - ((time.time() - starttime) % 60.0))


# ---------------- #
# ----- Main ----- #
# ---------------- #

if __name__ == '__main__':
    log.logger.info("----- Starting Dashboard -----")
    master_app_dict = ApplicationDict()
    master_cron_dict = CronDict()
    refresh_data(master_app_dict, master_cron_dict)
    make_wincrons(master_app_dict, master_cron_dict)
    get_beating_apps(master_app_dict)
    master_app_dict.init_templates()

    update_queue = Queue()
    update_event = Event()


    heartbeat_thread = Thread(target=heartbeat_recv, args=(update_queue, update_event)).start()
    # socketio.start_background_task(target=heartbeat_recv(update_queue))
    cron_thread = Thread(target=cron_watcher, args=(update_queue, update_event, master_cron_dict)).start()
    # socketio.start_background_task(target=cron_watcher(update_queue))
    updater_thread = Thread(target=state_updater, args=(update_queue, update_event, master_app_dict, master_cron_dict)).start()
    # updater_thread = socketio.start_background_task(target=state_updater(update_queue))
    # print("Is time monkeypatched?: " + str(eventlet.patcher.is_monkey_patched(time)) )
    # print("Is Queue monkeypatched?: " + str(eventlet.patcher.is_monkey_patched(Event)))
    socketio.run(app, port=5000, host = '192.168.70.56')
