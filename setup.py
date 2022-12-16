import os, re, json
from flask import Flask, request, render_template, Response
from werkzeug.utils import secure_filename
import backend.simulator as sim

global cpu, f_text, code_dict

ALLOWED_EXTENSIONS = {'yo'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__),'upload')

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    global cpu
    if request.method == 'POST':
        f = request.files.get('file')
        f_name = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, f_name))
        
        global f_text, code_dict
        code_dict = dict_trans(f_name)
        f_text = sim.get_ins("./upload/" + f_name)
        cpu, dic, err_msg, reg_file = sim.init_cpu(f_text)
        dic.update({'TEMP': reg_file})
        dic.update({"code_dict": code_dict})
        dic['ERR'] = err_msg

        return Response(json.dumps(dic), mimetype='application/json')


# 读取路径为 './upload/' + file_name 的文件，并通过正则表达式处理，返回字典
def dict_trans(file_name):
    file = open("./upload/" + file_name)
    instr = []
    line = 1
    while 1:
        line_text = file.readline()
        line_text.replace('\n','')
        if not line_text:
            break
        # 正则表达式处理
        str_temp = re.split('\s*\|', line_text)     # 按'|'分开
        if not re.match('^0x', str_temp[0]):
            pc = code = ''
        else:
            str_left = re.split(':\s*|\s*$', str_temp[0])   # 按照':'分开
            pc = str_left[0]
            code = str_left[1]
        text = line_text.replace('\t', '')
        text = line_text.replace(' ', '&nbsp')
        instr.append({'line':line, 'pc':pc, 'code':code, 'text':text})
        line += 1
    return instr


@app.route('/signal/')
def signal():
    global cpu
    signal = request.args.get('signal')
    if signal == 'instr':
        dic, err_msg, reg_file = sim.run_cpu(cpu, True)
    elif signal == 'stage':
        dic, err_msg, reg_file = sim.run_cpu(cpu, False)
    elif signal == 'reset':
        cpu, dic, err_msg, reg_file = sim.init_cpu(f_text)
    
    dic.update({'TEMP': reg_file})
    dic['ERR'] = err_msg
    dic['rsp_min'] = str(cpu.memory.rsp_min)
    # 直接用jsonify会按照键值排序后输出
    return Response(json.dumps(dic), mimetype='application/json')

@app.route('/last_step/')
def last_step():
    global cpu
    success, dic, err_msg, reg_file = sim.last_cycle(cpu)
    dic.update({'TEMP': reg_file})
    dic['ERR'] = err_msg
    dic['rsp_min'] = str(cpu.memory.rsp_min)
    dic['success'] = success
    return Response(json.dumps(dic), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)