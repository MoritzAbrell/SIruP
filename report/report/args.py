import argparse

parser = argparse.ArgumentParser(
    description="HTML report generator for SIruP sqlite database"
)

parser.add_argument(
    '-d',
    dest="DATABASE",
    type=str,
    required=True,
    help="Path to the SIrUP sqlite database"
)

parser.add_argument(
    '-o',
    dest="OUTFILE",
    type=str,
    default="report.html",
    help="Output filename of the HTML report"
)


def parse_args():
    args = parser.parse_args()
    return args
