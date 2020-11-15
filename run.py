import argparse
import datetime
import glob
import importlib
import json
import os
import subprocess
import sys
import time

suffix = None
args = None
tools = None
banner = '''
-- --- -. .. - --- .-.
-.-. --- .-.. .-.. . -.-. - --- .-.
'''

def install():
    with open('./requirements.json') as json_file:
        data = json.load(json_file)
        for requirement in data:
            name = requirement['name']
            print(f'[*] Installing: {name}')
            for command in requirement['commands']:
                print(f'[*] Executing: {command}')
                os.system(command)

def monitor():
    if not os.path.exists('./logs'):
        os.makedirs('./logs')
    global suffix
    suffix = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%SZ')

    procs = []
    for tool in tools:
        with open(f'./logs/tmp_{tool["name"]} {suffix}.json', 'w') as tmp_log_file:
            procs.append(subprocess.Popen(['sudo', '/usr/local/bin/unbuffer'] + tool['command'].split(), stdout=tmp_log_file))
    time.sleep(int(args.time))
    for proc in procs:
        proc.terminate()

    for tool in tools:
        output = ''
        print(f'\n[*] Collecting {tool["name"]}')
        with open(f'./logs/tmp_{tool["name"]} {suffix}.json', 'r') as tmp_log_file:
            module = importlib.import_module(f'modules.{tool["name"]}')
            output += module.parse(tmp_log_file)
        with open(f'./logs/{tool["name"]} {suffix}.json', 'w') as log_file:
            log_file.write(output)
            print(f'[*] Save as \'{log_file.name}\'')

    tmps = glob.glob('./logs/tmp_*')
    for tmp in tmps:
        os.remove(tmp)

def main():
    print(banner)

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--install',
            help='install requirements',
            action='store_true')
    parser.add_argument('-m', '--monitor',
            help='monitor process and file events',
            action='store_true')
    parser.add_argument('-t', '--time',
            help='set monitoring duration',
            action='store', dest='time')
    global args
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.error('no arguments provided')

    global tools
    with open('./tools.json', 'r') as tool_file:
        tools = json.load(tool_file)

    if args.install:
        install()
    if args.monitor:
        monitor()

if __name__ == '__main__':
    main()
