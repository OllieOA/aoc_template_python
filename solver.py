import argparse
import importlib
import logging
from pathlib import Path
import time
from typing import List, Callable

from utils.data_loader import DataLoader

_LOG_FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_LOG = logging.getLogger(__name__)

_LOG_STREAM_HANDLER = logging.StreamHandler()
_LOG_STREAM_HANDLER.setFormatter(_LOG_FORMATTER)

_LOG.addHandler(_LOG_STREAM_HANDLER)
_LOG.setLevel(logging.DEBUG)


class Solver:
    def __init__(self, use_sample: bool) -> None:
        self.use_sample = use_sample
        self.my_base_path = __file__
        self.day = -1
        self.logger = _LOG

    def part1(self, data: List) -> None:
        raise NotImplementedError("Implement this method in a child class!")

    def part2(self, data: List) -> None:
        raise NotImplementedError("Implement this method in a child class!")

    def _solve(self, solver: Callable, part: int, use_sample: bool) -> None:
        start_time = time.time()
        _LOG.info(f"| Part {part} | File I/O |")
        if use_sample:
            target_file = Path(self.my_base_path).parent / f"part{part}_sample.txt"
        else:
            target_file = Path(self.my_base_path).parent / f"part{part}_input.txt"

        assert target_file.exists(), f"Could not find {target_file}!"

        data = DataLoader(target_file).load_data()
        io_time = time.time()

        _LOG.info(f"| Part {part} | Solving |")
        result = solver(data)
        end_time = time.time()
        _LOG.info(
            f"| Solved! Answer: {result} in {(end_time-io_time) * 1000: 0.3f} ms! ({io_time-start_time * 1000:0.3f} ms for io)"
        )

    def solve(self):
        _LOG.info(f"| =------= DAY {self.day:02d} =------= |")
        self._solve(self.part1, 1, self.use_sample)
        self._solve(self.part2, 2, self.use_sample)
        _LOG.info(f"| =-----= COMPLETE =-----= |")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("d", type=int, help="Day to run (integer)")
    args.add_argument("-s", action="store_true", help="Run with sample input")
    args.add_argument("-a", action="store_true", help="Run all days")

    opts = args.parse_args()

    if opts.a:
        days = range(1, 26)
    else:
        days = [opts.d]

    for day in days:
        try:
            day_solver = importlib.import_module(f"day{day:02d}.solve_day")
            day_solver.solve_day(day, opts.s)
        except ImportError:
            _LOG.error(f"!!! DAY {day:02d} NOT IMPLEMENTED YET !!!")
