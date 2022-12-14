import os, re, json
from flask import Flask, request, render_template, jsonify, Response
from werkzeug.utils import secure_filename
import backend.simulator as sim

global cpu

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
    if request.method == 'POST':
        f = request.files.get('file')
        f_name = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, f_name))
        code_dict = dict_trans(f_name)

        f_text = sim.get_ins("./upload/" + f_name)
        global cpu
        cpu = sim.init_cpu(f_text)

        return jsonify(code_dict)


# 读取路径为 './upload/' + f_name 的文件，并通过正则表达式处理，返回字典
def dict_trans(f_name):
    file = open("./upload/" + f_name)
    ins = []
    line = 1
    while 1:
        line_text = file.readline()
        line_text.replace('\n','')
        if not line_text:
            break
        # 正则表达式处理
        str_temp = re.split('\s*\|', line_text)     # 按'|'分开
        text = str_temp[1]
        if not re.match('^0x', str_temp[0]):
            pc = code = ''
        else:
            str_left = re.split(':\s*|\s*$', str_temp[0])   # 按照':'分开
            pc = str_left[0]
            code = str_left[1]
        # 赋值与边界情况判定
        if text == '':
            continue
        flag = (code !='')
        ins.append({'line':line, 'pc':pc, 'code':code, 'text':text, 'flag':flag})
        line += 1
    return ins


@app.route('/signal/')
def signal():
    global cpu
    signal = request.args.get('signal')
    if signal == 'ins':
        dic, err_msg, _ = sim.run_cpu(cpu, True)
    elif signal == 'step':
        dic, err_msg, reg_file = sim.run_cpu(cpu, False)
        dic.update({'TEMP': reg_file})
        # print(dic)
    dic['ERR'] = err_msg
    # 直接用jsonify会按照键值排序后输出
    return Response(json.dumps(dic), mimetype='application/json')



if __name__ == '__main__':
    app.run(debug=True)