from lib.adb_utils import call_adb_command, get_output,\
     launch_monkey_event, call_shell_command
from lib.count import count_global_cs, rank
from lib.monkey import MonkeyDetails
from lib.progress_bar import ProgressBar

from collections import defaultdict
from time import sleep


APP = "my.package"


ITERATION = 10


def main():
    values = []
    bar = ProgressBar(100, 100, "PROGRESSING...")
    bar.update(0)
    bar_step = 100/ITERATION
    seed_to_details = defaultdict()
    for i in range(ITERATION):
        log_thread = call_adb_command("log", "-c")
        log_thread.wait()
        (seed, monkey_thread) = launch_monkey_event(APP,
                                                    events="1000",
                                                    throttle="300")
        monkey_thread.wait()
        monkey_output = get_output(monkey_thread)
        output = get_output(call_adb_command("log", "-d"))
        global_count = count_global_cs(output)
        values.append((seed, global_count))
        seed_to_details[seed] = MonkeyDetails(monkey_output)

        stop_thread = call_shell_command("stop", APP)
        stop_thread.wait()
        reset_thread = call_shell_command("reset", APP)
        reset_thread.wait()
        bar.update((i + 1) * bar_step)

        sleep(5)

    set_top_3 = rank(values)

    for seed in set_top_3:
        print("SEED %s" % seed)
        print(seed_to_details[seed])
        print("#"*40)


if __name__ == '__main__':
    main()
