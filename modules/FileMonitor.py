import json

ignore_list = [
        'FileMonitor',
        'ProcessMonitor'
        ]

def parse(tmp_log_file):
    blocks = []
    datas = tmp_log_file.read().split('}\n{')
    for data in datas[:-1]:
        if data == '':
            break
        if data[0] != '{':
            data = '{' + data
        if data[-1] != '}':
            data = data + '}'
        try:
            message = json.loads(data)
            if (any(item in message['file'].get('destination', '(null)') for item in ignore_list) or
                    any(item in message['file']['process'].get('path', '(null)') for item in ignore_list)):
                continue
            block = {}
            block['timestamp'] = message['timestamp']
            block['event type'] = message['event']
            block['source path'] = message['file'].get('source', '(null)')
            block['destination path'] = message['file'].get('destination', '(null)')
            block['path'] = message['file']['process'].get('path', '(null)')
            block['pid'] = message['file']['process']['pid']
            block['uid'] = message['file']['process']['uid']
            block['ancestors'] = message['file']['process']['ancestors']
            block['signing info'] = message['file']['process']['signing info']
            blocks.append(block)
        except:
            continue
    return json.dumps(blocks, indent=2)
