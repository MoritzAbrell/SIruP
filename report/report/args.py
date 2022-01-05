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
    default="report",
    help="Output filename of the report. A HTML and CSV file will be generated"
)

parser.add_argument(
    '--full',
    dest="FULL",
    action='store_true',
    help="Including country analysis. This may takes a while because of API limits"
)


def parse_args():
    args = parser.parse_args()
    return args
