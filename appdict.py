


class ApplicationDict:

    def __init__(self):
        self.clear()

    def clear(self):
        self.applications = {}
        self.unindexed_apps = []
        self.suites = {}
        self.datacenters = {}
        self.desks = {}
        self.suite_list = []
        self.datacenter_list = []
        self.desk_list = []
        self.simple_desk_list = []
        self.homelist = []

    def init_templates(self):
        self.set_unindexed_apps()
        self.set_suites()
        self.set_suite_list()
        self.set_datacenters()
        self.set_datacenter_list()
        self.set_desks()
        self.set_desk_list()
        self.set_simple_desk_list()
        self.set_home_list()

    def get_app(self, key):
        return self.applications[key]

    def get_apps(self):
        return self.applications

    def add_app(self, key, app):
        self.applications[key] = app
        self.applications[key].change_color()
        self.init_templates()

    def update_app_status(self, key, type, new_status):
        color = self.applications[key].update_status(type, new_status)
        self.init_templates()
        return color

    def set_app_cron(self, key, type, dayweek, minute, hour):
        self.applications[key].set_cron(type, dayweek, minute, hour)

    def remove_app(self, key):
        return_value = self.applications.pop(key, None)
        if return_value:
            self.init_templates()
        return return_value

    def set_unindexed_apps(self):
        self.unindexed_apps = []
        for key, app in self.applications.items():
            self.unindexed_apps.append(vars(app))

        return self.unindexed_apps

    def set_suites(self):

        # ----- Making suite organized data structure: {sapphire:[{"name": ,"suite": ,"desk": }, ...], ...} ----- #
        self.suites = {}

        for app_copy in self.unindexed_apps:
            app = app_copy.copy()
            app["display_name"] = app["name"]
            if app["suite"] not in self.suites:
                self.suites[app["suite"]] = []
            self.suites[app["suite"]].append(app)

        for key in self.suites:
            self.suites[key] = sorted(self.suites[key], key=lambda k: (k['display_name'], k['host']))

        #suites['sapphire'] = sorted(suites['sapphire'], key=lambda k: k['name'])

        return self.suites

    def set_datacenters(self):

        self.datacenters = {}

        for app_copy in self.unindexed_apps:
            app = app_copy.copy()
            app["display_name"] = app["suite"] + "-" + app["name"]
            if app["datacenter"] not in self.datacenters:
                self.datacenters[app["datacenter"]] = []
            self.datacenters[app["datacenter"]].append(app)

        for key in self.datacenters:
            self.datacenters[key] = sorted(self.datacenters[key], key=lambda k: (k['display_name'], k['host']))


        return self.datacenters

    def set_desks(self):

        self.desks = {}

        for app_copy in self.unindexed_apps:
            app = app_copy.copy()
            app["display_name"] = app["suite"] + "-" + app["name"]
            if app["desk"] not in self.desks:
                self.desks[app["desk"]] = []
            self.desks[app["desk"]].append(app)

        for key in self.desks:
            self.desks[key] = sorted(self.desks[key], key=lambda k: (k['display_name'], k['host']))


        return self.desks

    def set_suite_list(self):

        # ----- Making suite organized data structure: ["sapphire", [{"app_name": ,"suite": ,"desk": }, ...], ...] ----- #

        self.suite_list = []

        for app in self.suites:
            if self.suite_list:
                for index, suite in enumerate(self.suite_list):
                    if len(self.suites[app]) > len(suite[1]):
                        self.suite_list.insert(index, [app, self.suites[app]])
                        break;

                    if index == (len(self.suite_list) - 1):
                        self.suite_list.append([app, self.suites[app]])
                        break;
            else:
                self.suite_list.append([app, self.suites[app]])

        return self.suite_list

    def set_datacenter_list(self):
        self.datacenter_list = []

        for datacenter in self.datacenters:
            if self.datacenter_list:
                for index, dc_list in enumerate(self.datacenter_list):
                    if len(self.datacenters[datacenter]) > len(dc_list[1]):
                        self.datacenter_list.insert(index, [datacenter, self.datacenters[datacenter]])
                        break;

                    if index == (len(self.datacenter_list) - 1):
                        self.datacenter_list.append([datacenter, self.datacenters[datacenter]])
                        break;

            else:
                self.datacenter_list.append([datacenter, self.datacenters[datacenter]])

        return self.datacenter_list

    def set_desk_list(self):
        self.desk_list = []

        for desk in self.desks:
            if self.desk_list:
                for index, d_list in enumerate(self.desk_list):
                    if len(self.desks[desk]) > len(d_list[1]):
                        self.desk_list.insert(index, [desk, self.desks[desk]])
                        break;
                    if index == (len(self.desk_list) - 1):
                        self.desk_list.append([desk, self.desks[desk]])
                        break;

            else:
                self.desk_list.append([desk, self.desks[desk]])


        return self.desk_list

    def set_home_list(self):
        self.home_list = []
        otherlist = []

        for app in self.suites:
            if len(self.suites[app]) > 9:
                if self.home_list:
                    for index, suite in enumerate(self.home_list):
                        if len(self.suites[app]) > len(suite[1]):
                            self.home_list.insert(index, [app, self.suites[app]])
                            break;

                        if index == (len(self.home_list) - 1):
                            self.home_list.append([app, self.suites[app]])
                            break;
                else:
                    self.home_list.append([app, self.suites[app]])
            else:
                for line_copy in self.suites[app]:
                    line = line_copy.copy()
                    line["display_name"] = line["suite"] + "-" + line["name"]
                    otherlist.append(line)

        otherlist = sorted(otherlist, key=lambda k: (k['display_name'], k['host']))

        self.home_list.append(["other", otherlist])


        """
        for index, suite in enumerate(self.home_list):
            if len(otherlist) > len(suite[1]):
                self.home_list.insert(index, ["other", otherlist])
                break;

        else:
            self.home_list.append(["other", otherlist])
        """
        return self.home_list

    def set_simple_desk_list(self):
        self.simple_desk_list = []
        for line in self.desk_list:
            self.simple_desk_list.append(line[0])

        return self.simple_desk_list


class Application:
    def __init__(self, host, suite, name, desk="ssvcs", datacenter="default", hb_status="down"):
        self.host = host
        self.suite = suite
        self.name = name
        self.desk = desk
        self.datacenter = datacenter
        self.hb_status = hb_status
        self.cron_status = "down"
        self.lr_status = "down"
        self.cron = {}
        self.cron_list = {}
        self.color = "#3b3b3b"

    def change_color(self):
        if (self.suite in ["pricefeeder", "sapphire"]) and (self.hb_status == "up" and self.lr_status == "down"):
            self.color = "#f4ee42"
        elif (self.suite in ["pricefeeder", "sapphire"]) and (self.hb_status == "down" and self.lr_status == "up"):
            self.color = "#720000"
        elif self.hb_status == "up" and self.cron_status == "up":
            self.color = "#00441c"
        elif self.hb_status == "up" and self.cron_status == "down":
            self.color = "#012766"
        elif self.hb_status == "down" and self.cron_status == "up":
            self.color = "#720000"
        else:
            self.color = "#3b3b3b"

        return self.color

    def update_status(self, type, new_status):
        if type == "lr_status":
            self.lr_status = new_status
        elif type == "cron_status":
            self.cron_status = new_status
        elif type == "hb_status":
            self.hb_status = new_status
        else:
            return None

        color = self.change_color()
        return color

    def set_cron(self, type, dayweek, minute, hour):
        self.cron[type] = {"dayweek": dayweek, "minute": minute, "hour": hour}


class CronDict:

    fresh_cron_dict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

    def __init__(self):
        self.cron_dict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

    def add_entry(self, day, cron_time, key, type):
        if not self.cron_dict[day].get(cron_time):
            self.cron_dict[day][cron_time] = []
        self.cron_dict[day][cron_time].append({"app": key, "status": type})

    def check_time(self, day, cron_time):
        if self.cron_dict[day].get(cron_time):
            return True
        else:
            return False

    def get_apps(self, day, cron_time):
        return self.cron_dict[day][cron_time]

    def clear(self):
        self.cron_dict = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}}

    def get_crons(self):
        return self.cron_dict
