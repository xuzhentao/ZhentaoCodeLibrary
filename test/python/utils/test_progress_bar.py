from src.python.utils.ProgressBar import ProgressBar


def test_progress_bar():
    progressbar = ProgressBar(int_total=123450,  # [must] This is the estimation of the total amount of count.
                              float_progressDelta=0.01,
                              # (optional)	This is the delta of reporting, e.g. 0.1 will report 1/0.1 = 10 times.
                              ID="PROGRESSBAR_1"  # (optional)	This is only for showing the progress.
                              )
    for i in range(123450):  # This is a loop, totally loop for 12345times.
        progressbar.count()


if __name__ == "__main__":
    test_progress_bar()
