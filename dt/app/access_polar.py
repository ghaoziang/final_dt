from __future__ import print_function

from app.utils import load_config, pretty_print_json
from accesslink import AccessLink
from app.tcx2csv import tcx_to_csv
import os


'''
try:
    input = raw_input
except NameError:
    pass
'''
config_path = os.path.join(os.getcwd(), "device_config")
CONFIG_FILENAME = os.path.join(config_path, "config.yml")
polar_path = "/home/gaoziang/databox/polar_h10/"


class PolarAccessLinkExample(object):
    """Example application for Polar Open AccessLink v3."""

    def __init__(self):
        self.config = load_config(CONFIG_FILENAME)

        if "access_token" not in self.config:
            print("Authorization is required. Run authorization.py first.")
            return

        self.accesslink_ = AccessLink(client_id=self.config["client_id"],
                                     client_secret=self.config["client_secret"])

        self.running = True

    def get_exercises_list(self):
        transaction = self.accesslink_.training_data.create_transaction(user_id=self.config["user_id"],
                                                                        access_token=self.config["access_token"])
        if not transaction:
            print("No new exercises available.")
            return

        resource_urls = transaction.list_exercises()["exercises"]
        exercises_list = []
        for url in resource_urls:
            exercise_summary = transaction.get_exercise_summary(url)
            print(type(exercise_summary))
            exercises_list.append(exercise_summary)

        for url in resource_urls:
            exercise_summary = transaction.get_exercise_summary(url)
            print("Exercise summary:")
            pretty_print_json(exercise_summary)

            eid = exercise_summary.get('id')
            print(eid)
            tcx = transaction.get_tcx(url)
            print(tcx)
            path = os.path.join(polar_path, str(eid) + '.csv')
            tcx_to_csv(tcx, path)

        transaction.commit()

        return resource_urls, exercises_list


if __name__ == "__main__":
    PolarAccessLinkExample()