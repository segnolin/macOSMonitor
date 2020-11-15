# macOSMonitor

macOSMonitor is the monitoring scripts for process and filesystem events. For simplicity, we only include two monitoring tools. Users can follow the instruction below to add their own tools.

## Getting Started

Simply cloning the project.

```
git clone https://github.com/segnolin/macOSMonitor.git
```

### Prerequisites

- Scripts require Python 3.6+
- Endpoint Security API requires macOS 10.15+

### Install Tool Requirements

Go to the project directory.

```
cd macOSMonitor
```

Run the installation script.

```
python3 run.py --install
```

### Monitoring

Run the monitoring script with root permission with the monitoring duration. (e.g. 10 seconds)

```
sudo python3 run.py --monitor --time 10
```

You will see the path of the log file as below after monitoring:

```
[*] Save as './logs/[Tool Name] [YYYY]-[mm]-[dd]T[HH]_[MM]_[SS]Z.json'
```

## Documentation

This section shows to tweak and add the functionality of the monitoring tools.

### Usage of macOSMonitor

```
usage: run.py [-h] [-i] [-m] [-t TIME]

optional arguments:
  -h, --help            show this help message and exit
  -i, --install         install requirements
  -m, --monitor         monitor process and file events
  -t TIME, --time TIME  set monitoring duration
```

### Adding Tool

The procedure of adding tools consists of the following three parts.
Each part is necessary for the tools to work properly.

#### Tool (or Dependency) Installation

The following properties of installation of tool (or dependency) can be found in `requirements.json`:

```
[
  {
    "name": string (Name of tool or dependency),
    "commands": array[string] (series of commands that install the tool or dependency),
  },
  ...
]
```

#### Tool Execution

The following properties of monitoring tool can be found in `tools.json`:

```
[
  {
    "name": string (Name of tool, and should be the same as the name of executable),
    "command": string (One line command to run the monitoring tool)
  },
  ...
]
```

#### Tool Output Parsing

Each monitoring tool should have its parsing script for output file consistency.
The script should be written in Python 3.6+ with the file name `[Name of tool].py` inside `./modules` folder.
The parsing function prototype describes as below:

```py
def parse(tmp_log_file):
  # parse the temporary log file and return the output as string
  return output_str
```

## Reference

* [objective-see/ProcessMonitor](https://github.com/objective-see/ProcessMonitor)
* [objective-see/FileMonitor](https://github.com/objective-see/FileMonitor)
