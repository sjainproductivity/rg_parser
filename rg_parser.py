#!/bin/python
import platform
import argparse
import sys
import configparser

only_files, match_count, text_search, ignore_case, word_match = None, None, None, None, None
search_filters = None


def read_config(configfile):
    """
    Reads configuration file and loads respective configuration
    """
    global only_files, match_count, text_search, ignore_case, word_match, search_filters
    config = configparser.ConfigParser()
    try:
        config.read(configfile)
        if len(config.sections()) == 0:
            raise Exception("Config file is empty")

        only_files = (False, True)[config['default']['only_files'] == 'True']
        match_count = (False, True)[config['default']['match_count'] == 'True']
        text_search = (False, True)[config['default']['text_search'] == 'True']
        ignore_case = (False, True)[config['default']['ignore_case'] == 'True']
        word_match = (False, True)[config['default']['word_match'] == 'True']
        search_filters = dict(config.items('search_filter'))
        config.remove_section('search_filter')
    except KeyError as ker:
        print(f"Error: Can't find the key {ker} in search_config.ini")
        config = None
    except Exception as er:
        print(f"Error: Can't valid sections in search_config.ini")
        config = None
    finally:
        return config


def __get_search_filter(search_section):
    # Get file filters from configuration file if not default to section
    global search_filters
    file_filter = None
    try:
        if search_filters.get(search_section) == None:
            file_filter = search_section+".*"
        else:
            file_filter = search_filters.get(search_section)
    except KeyError as ker:
        print(f"Error: Can't find the key {ker} in search_config.ini")
    finally:
        return file_filter


def __format_response(text):
    """
    Text formatter, appends --
    """
    p_response = "-"*20+text.upper() + "-"*20
    return p_response


def __write_file(decorated):
    """
    Decorator to write the file
    """
    file_name = None

    def script_wrapper(config, os):
        global file_name
        file_data = decorated(config)
        file_name = "analysis.sh"
        if "window" in os.lower():
            file_name = "analysis.bat"
        with open(file_name, 'w') as f:
            f.writelines(file_data)
        print("Analysis script generated. Please execute {}".format(file_name))
    return script_wrapper


def command_builder(platform):
    pass


@__write_file
def __build_script(config):
    global only_files, match_count, text_search, ignore_case, word_match
    shell_cmds = ['SEARCH_DIRECTORY=""\n', 'OUTPUT_DIRECTORY=""\n']

    invocations = ["if [ \"$1\" ]\n",
                   "then\n\tif [ \"$2\" ]\n\tthen\n\t\tSEARCH_DIRECTORY=\"$1\"\n\t\tOUTPUT_DIRECTORY=\"$1\"\n\t\tECHO 'SEARCH DIRECTORY: \"$SEARCH_DIRECTORY\"'\n\tECHO 'OUTPUT DIRECTORY: \"$OUTPUT_DIRECTORY\"'\n"]
    config.remove_section('default')

    for search_section in config.sections():
        for key, value in config[search_section].items():
            value = value.strip('"')
            key = key.strip('"')
            invocations.append(f"\t\t{key.lower().replace(' ','_')}\n")
            out_file = search_section+'_parser.log'

            search_filter = __get_search_filter(search_section.lower())

            echo_out = __format_response(key+":"+value)
            shell_cmds.append("\n#Search for {}\n\n".format(key))
            shell_cmds.append(f"{key.lower().replace(' ','_')} ()")
            shell_cmds.append("{\n")
            shell_cmds.append(
                'echo "Searching {} OUTPUT- {}"'.format(echo_out, out_file))
            shell_cmds.append("\n")
            shell_cmds.append(
                'echo "{}" >> "$OUTPUT_DIRECTORY\{}"'.format(echo_out, out_file))
            shell_cmds.append("\n")
            command = "rg "
            if match_count:
                shell_cmds.append(
                    "count=$(rg -c -w '{}' -g '{}' \"$SEARCH_DIRECTORY\" |wc -l)".format(value, search_filter))
                shell_cmds.append("\n")
                shell_cmds.append('echo "Total Matches for {} ${} >> "$OUTPUT_DIRECTORY\{}" '.format(
                    value, "count", out_file))
                shell_cmds.append("\n")
            if ignore_case:
                command += "-i "
            if word_match:
                command += "-w '{}' ".format(value)
            if only_files:
                command += "-l "
            command += "-g '{}' \"$SEARCH_DIRECTORY\" >> \"$OUTPUT_DIRECTORY\{}\"".format(
                search_filter, out_file)
            command += "\n}\n"
            shell_cmds.append(command)
            shell_cmds.append("\n")
    invocations.extend(
        ["\telse\n", "\t\techo 'ERROR: Please provide output directory path'\n", "\tfi\n", "else\n", "\techo 'ERROR: Please provide search directory path'\n", "fi\n"])
    shell_cmds.extend(invocations)
    return shell_cmds


@__write_file
def __build_script_win(config):
    global only_files, match_count, text_search, ignore_case, word_match
    batch_cmds = ['ECHO OFF\n', 'SET SEARCH_DIRECTORY=""\n',
                  'SET OUTPUT_DIRECTORY=""\n']

    invocations = ["IF %1.==. (\n ECHO 'ERROR: Please provide search directory path'\n GOTO TERMINATE \n ) ELSE ( \n IF %2.==. ( \n ECHO 'ERROR: Please provide outuput directory path'\n GOTO TERMINATE \n ) ELSE ( \n GOTO EXECUTION \n)\n)",
                   "\n:EXECUTION\n\tSET SEARCH_DIRECTORY=%1%\n\tSET OUTPUT_DIRECTORY=%2%\n\tECHO 'SEARCH DIRECTORY: %SEARCH_DIRECTORY%'\n\tECHO 'OUTPUT DIRECTORY: %OUTPUT_DIRECTORY%'"]
    batch_cmds.extend(invocations)
    config.remove_section('default')

    for search_section in config.sections():
        for key, value in config[search_section].items():
            value = value.strip('"')
            key = key.strip('"')
            out_file = search_section+'_parser.log'

            search_filter = __get_search_filter(search_section.lower())

            echo_out = __format_response(key+":"+value)
            batch_cmds.append("\n\t@REM Search for {}\n".format(key))
            # defining function
            batch_cmds.append("\n")
            batch_cmds.append(
                '\techo "Searching {} OUTPUT- {}"'.format(echo_out, out_file))
            batch_cmds.append("\n")
            batch_cmds.append(
                '\techo "{}" >> %OUTPUT_DIRECTORY%\{}'.format(echo_out, out_file))
            batch_cmds.append("\n")
            command = "\trg "
            if match_count:
                batch_cmds.append(
                    'count=$(rg -c -w "{}" -g "{}" %SEARCH_DIRECTORY% |wc -l)'.format(value, search_filter))
                batch_cmds.append("\n")
                batch_cmds.append('echo "Total Matches for {} ${} >> %OUTPUT_DIRECTORY%\{}" '.format(
                    value, "count", out_file))
                batch_cmds.append("\n")
            if ignore_case:
                command += "-i "
            if word_match:
                command += '-w "{}" '.format(value)
            if only_files:
                command += "-l "
            command += '-g "{}" %SEARCH_DIRECTORY% >> %OUTPUT_DIRECTORY%\{}'.format(
                search_filter, out_file)

            batch_cmds.append(command)
            batch_cmds.append("\n")
    batch_cmds.append("\n\tGOTO TERMINATE\n:TERMINATE\n\tEXIT /B 0")

    return batch_cmds


def generate_config(filename):
    config = configparser.ConfigParser()

    config['default'] = {
        'only_files': False,
        'match_count': False,
        'text_search': True,
        'ignore_case': True,
        'word_match': True
    }
    config['search_filter'] = {
        'all': '*.*',
        'error': '*.*',
        'warn':  '*.*',
    }
    config['error'] = {
        'ERROR': 'ERROR'
    }
    config['warn'] = {
        'WARN': 'WARN'
    }
    with open(filename, 'w') as configfile:
        config.write(configfile)
    print(f"Cofniguration file {filename} generated")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalid arguments provided")
        sys.exit()
    if len(sys.argv) > 3:
        print("To many arguments provided")
        sys.exit()
    else:
        parser = argparse.ArgumentParser("CARA Logs Analysis")
        parser.add_argument('--config', '-c', type=str,
                            help="Generates a configuration file. Ex -c config.ini")
        parser.add_argument('--analysis', '-a', type=str,
                            help="Generates an analysis.sh script. Ex -g config.ini")
        args = parser.parse_args()
        if args.config != None:
            generate_config(args.config)
        if args.analysis != None:
            config = read_config(args.analysis)
            if config == None:
                print('Generate config file with -c search_config.ini')
                sys.exit(-1)
            # Get OS details to determine windows/linux
            os = platform.system().lower()
            if "windows" in os:
                __build_script_win(config, os)
            elif "linux" in os:
                __build_script(config, os)
            else:
                print("Platform {} not supported.", platform.system())
