### Table Of Contents
 * [Use-Case](#use-case)
 * [Setup](#setup)
    * [Pre-Requisites](#pre-requisites)
    * [Validation](#validation)
    * [Usage](#usage)
 * [Troubleshooting](#troubleshooting)
    * [Windows](#windows)
  * [Report Issues](#report-issues)



# User Guide  
The guide is to provide an introduction to the user about rg_parser python script, used to generate analysis.bat/sh script based on configuration provided by user.  

> Dependencies  
>> rg_parser uses [ripgrep](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md "The fastest search") underneath to make search in directory
---  

### Use-Case
- Allows documentation of logs pattern in configuration, making search consistent and reusable
- Allows documentation of logs pattern for cases. You can keep versioning *.ini file as you progress
- Helps in knowledge transfer among workers. The *.ini file generate can be used by other workers with same setup

---  
### Setup
#### Pre Requisites
      - On Windows/Linux Install Python 3.6 or higher
      - Install ripgrep for appropriate OS [ripgrep Installation](https://github.com/BurntSushi/ripgrep#installation)
        - **Note** :On Windows, one can download [precompiled binaries](https://github.com/BurntSushi/ripgrep/releases/tag/13.0.0) and set the environment PATH variable 
      - Clone the repository rg_parser, i.e. git clone https://github.com/sjainproductivity/rg_parser.git or download the zip
  
#### Validation
    1. Validate python is installed: 
        $python -V
    2. Validate ripgrep is installed:
        $rg -V
      

### Usage
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


### Troubleshooting

#### Windows
- 'rg' is not recognized as an internal or external command : The rg.exe is not configured in PATH.

### Report Issues
- [rg_parser_issues](https://github.com/sjainproductivity/rg_parser/issues)