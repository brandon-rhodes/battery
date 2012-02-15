"""Command-line battery."""

import battery.build
import sys

def main():
    versions = sys.argv[1:] or (
        '1.5.2', '1.6.1', '2.0.1', '2.1.3', '2.2.3', '2.3.7',
        '2.4.6', '2.5.6', '2.6.7', '2.7.2', '3.1.4', '3.2.2'
        )
    for version in versions:
        battery.build.download(version)
        battery.build.untar(version)
        battery.build.cmmi(version)
