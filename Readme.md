# Project Summary
The python script is used to generate analysis.bat/sh script based on configuration provided by user. The script will be using ripgrep to search patterns described in logs and generate various [section_name]_parser.log file.

### USE CASE
- Allows documentation of logs pattern in configuration, making search consistent and repetable
- Allows documentation of logs pattern for each case, just versioned the INI file
- Helps in knowledge transfer among workers
  
## ToDo

## Pre-Requisites
- On Windows/Linux Install Python 3.6 or higher
- Install ripgrep for appropriate OS [ripgrep Installation](https://github.com/BurntSushi/ripgrep#installation)
  - For windows one can download precompiled binaries and set the PATH variable
## Setup


## Usage
```
usage: CARA Logs Analysis [-h] [--config CONFIG] [--analysis ANALYSIS]

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
                        Generates a configuration file. Ex -c config.ini
  --analysis ANALYSIS, -a ANALYSIS
                        Generates an analysis.(sh|bat) script file from configuration file. Ex -a config.ini
```
- Example: Generating config file template
  ```
  python -c/--config CONFIG_FILE_NAME.ini

  OUTPUT
  [default]
    only_files = False
    match_count = False
    text_search = True
    ignore_case = True
    word_match = True

    [search_filter]
    all = *.*
    error = *.*
    warn = *.*

    [error]
    error = ERROR

    [warn]
    warn = WARN
  ```
- Generate scripts based on INI file
  ```
    python -a/--analysis CONFIG_FILE_NAME.ini
  ```
- Accept output directory
- Linking 


## Troubleshooting

### Windows
- 'rg' is not recognized as an internal or external command : The rg.exe is not configured in PATH.