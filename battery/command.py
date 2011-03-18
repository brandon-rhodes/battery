"""Command-line battery."""

import battery.build

def main():
    for version in ('1.5.2', '1.6.1', '2.0.1', '2.1.3', '2.2.3', '2.3.7',
                    '2.4.6', '2.5.5', '2.6.6', '2.7.1', '3.1.3', '3.2'):
        battery.build.download(version)
        battery.build.untar(version)
        battery.build.cmmi(version)
