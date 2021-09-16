########################################
# Filename: Class_ProgressBar.py (Python Version = 3.5)
# Author: Zhentao Xu (frankxu@umich.edu)
# Description: This class is to control the progress,
# License: This code is part of the Deep Learning Sensor Abnormal Detection System. Please contact Zhentao Xu before any modifications, or technical support.
########################################


# This is a progress bar class. Use to count and report the training progress. This is used to make the training more visible.

class Class_ProgressBar:
    def __init__(self, int_total, float_progressDelta=0.1, ID='PROGRESSBAR'):
        self.ID = ID  # the ID of this progress
        self.int_total = int_total  # the expected total count.
        self.int_count = 0  # the current count
        self.float_progress = 0  # the current progress = current count / total count.
        self.float_progressDelta = float_progressDelta  # the delta in progress, for ex. 0.1 will generate show report at 10%, 20%, ... 100%.

    def count(self):  # call this function to update the progress.
        self.int_count = self.int_count + 1
        if (self.int_count * 1.0 / self.int_total >= self.float_progress):
            print("[" + self.ID + "] Progress Report  : " + str(int(self.float_progress * 100)) + "%")
            self.float_progress = self.float_progress + self.float_progressDelta


########## Sample Call ########## :
if __name__ == "__main__":

    progressbar = Class_ProgressBar(int_total=12345000,
                                    # [must]		This is the estimation of the total amount of count.
                                    float_progressDelta=0.01,
                                    # (optional)	This is the delta of reporting, e.g. 0.1 will report 1/0.1 = 10 times.
                                    ID="PROGRESSBAR_1"  # (optional)	This is only for showing the progress.
                                    )
    for i in range(12345000):  # This is a loop, totally loop for 12345times.
        progressbar.count();
