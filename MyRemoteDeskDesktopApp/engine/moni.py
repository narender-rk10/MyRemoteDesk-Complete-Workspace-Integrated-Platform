from __future__ import print_function
import time
import json
import datetime
import sys
import plotly.graph_objects as go
import mysql.connector
import datetime

if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto

connectiondb = mysql.connector.connect(host="host", user="user", password="password", database="database", port=3306)
cursordb = connectiondb.cursor()

b = list()
print(connectiondb)

class AcitivyList:
    def __init__(self, activities):
        self.activities = activities

    def initialize_me(self):
        activity_list = AcitivyList([])
        with open('activities.json', 'r') as f:
            data = json.load(f)
            activity_list = AcitivyList(
                activities=self.get_activities_from_json(data)
            )

        return activity_list

    def get_activities_from_json(self, data):
        return_list = []
        for activity in data['activities']:

            return_list.append(
                Activity(
                    name=activity['name'],
                    time_entries=self.get_time_entires_from_json(activity),
                )
            )
        self.activities = return_list
        return return_list

    def get_time_entires_from_json(self, data):
        return_list = []
        for entry in data['time_entries']:
            return_list.append(
                TimeEntry(
                    start_time=parser.parse(entry['start_time']),
                    end_time=parser.parse(entry['end_time']),
                    days=entry['days'],
                    hours=entry['hours'],
                    minutes=entry['minutes'],
                    seconds=entry['seconds'],
                )
            )
        self.time_entries = return_list
        return return_list

    def serialize(self):
        return {
            'activities': self.activities_to_json()
        }

    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())

        return activities_


class Activity:
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'name': self.name,
            'time_entries': self.make_time_entires_to_json()
        }

    def make_time_entires_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())

        return time_list


class TimeEntry:
    def __init__(self, start_time, end_time, days, hours, minutes, seconds):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def _get_specific_times(self):
        self.days, self.seconds = self.total_time.days, self.total_time.seconds
        self.hours = self.days * 24 + self.seconds // 3600
        self.minutes = (self.seconds % 3600) // 60
        self.seconds = self.seconds % 60

    def serialize(self):
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }


def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]


def get_active_window():
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


def get_chrome_url():
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return 'https://' + edit.GetValuePattern().Value
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


def show_activity():

    b = list()
    d = list()
    try:
        with open('activities.json', 'r') as jsonfile:
            a = json.load(jsonfile)
            e = a['activities']
    except Exception:
        print("no json data")
        exit(0)

    for i in e:
        b.append(i['name'])

    tot = 0

    for i in e:
        sed = 0
        for j in i["time_entries"]:
            sed = sed + int(j["minutes"])*60 + \
                int(j["seconds"])+int(j["hours"])*3600
            tot = tot+sed
        d.append(sed)

    kek = time.strftime("%H:%M:%S", time.gmtime(tot))
    kek = "Time used : "+kek
    print(b)
    print(d)
    combineBD = zip(b, d)
    zipped_list = list(combineBD)

    return zipped_list


def erase():
    open("activities.json", "w").close()


def record(active_window_name, activity_name, start_time, activeList, first_time, e_id, o_id):
    try:
        al = activeList.initialize_me()
    except Exception:
        print('No json')

    try:
        while True:
            previous_site = ""
            if sys.platform not in ['linux', 'linux2']:
                new_window_name = get_active_window()
                if 'Google Chrome' in new_window_name:
                    new_window_name = url_to_name(get_chrome_url())
            if sys.platform in ['linux', 'linux2']:
                new_window_name = l.get_active_window_x()
                if 'Google Chrome' in new_window_name:
                    new_window_name = l.get_chrome_url_x()

            if active_window_name != new_window_name:
                print(active_window_name)
                activity_name = active_window_name
                al = activity_name
                print(al)
                print(type(al))
                ct = datetime.datetime.now()
                sql = "INSERT INTO monitoring (m_title, m_log_ts, e_id_id, o_id_id) VALUES (%s, %s, %s, %s)"
                val = (al, ct, e_id, o_id)
                cursordb.execute(sql, val)
                connectiondb.commit()
                print(cursordb.rowcount, "record inserted.")

                if not first_time:
                    end_time = datetime.datetime.now()
                    time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                    time_entry._get_specific_times()

                    exists = False
                    for activity in activeList.activities:
                        if activity.name == activity_name:
                            exists = True
                            activity.time_entries.append(time_entry)

                    if not exists:
                        activity = Activity(activity_name, [time_entry])
                        activeList.activities.append(activity)
                    with open('activities.json', 'w') as json_file:
                        json.dump(activeList.serialize(), json_file,
                                  indent=4, sort_keys=True)
                        start_time = datetime.datetime.now()
                first_time = False
                active_window_name = new_window_name

            time.sleep(1)

    except KeyboardInterrupt:
        with open('activities.json', 'w') as json_file:
            json.dump(activeList.serialize(), json_file,
                      indent=4, sort_keys=True)


def mainRecord(e_id, o_id):
    active_window_name = str()
    activity_name = ""
    start_time = datetime.datetime.now()
    activeList = AcitivyList([])
    first_time = True
    record(active_window_name, activity_name,start_time, activeList, first_time, e_id, o_id)
