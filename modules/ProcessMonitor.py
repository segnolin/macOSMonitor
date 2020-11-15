import json

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
            block = {}
            block['timestamp'] = message['timestamp']
            block['event type'] = message['event']
            block['path'] = message['process'].get('path', '(null)')
            block['pid'] = message['process']['pid']
            block['uid'] = message['process']['uid']
            block['args'] = message['process']['arguments']
            block['ancestors'] = message['process']['ancestors']
            block['signing info'] = message['process'].get('signing info', '(null)')
            blocks.append(block)
        except:
            continue
    return json.dumps(blocks, indent=2)
