var code_dict;   // 指令code_table的字典
var stage = 0;   // 用于标记单阶段运行，下一阶段为哪一阶段
const STAGE_MAX = 6;
const REGISTER_LIST = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', '/']
const CC_LIST = ['ZF', 'SF', 'OF']
const STAGE_NAME = ['FETCH', 'DECODE', 'EXECUTE', 'MEMORY', 'WRITE BACK', 'PC UPDATE']
var run_flag = 0;
var rsp_init = 0;     // rsp初始值
var last_res;    // 上一步的字典


function upload() {
    var file = new FormData();
    file.append("file", $("#file")[0].files[0]);
    $.ajax({
        url: 'upload/',
        type: 'post',
        data: file,
        contentType: false,
        processData: false,
        success: function (res) {     // response 回调函数
            code_dict = res.code_dict;
            last_res = res;
            init();
            $("#code").html(content(code_dict, 0));
            $("#memory").html(content(res, 5));
            mem_code_set(res);
            code_highlight(res, 'init');
            run_flag = 1;
            rsp_init = 0;
        }
    })
}


// signal='instr'：运行一个指令；signal='stage'：运行一个阶段，传参给后端
function next(signal) {
    switch (run_flag) {
        case 0:
            alert("ALERT: You should upload files first!"); break;
        case 1: {
            // 执行一条指令
            if (signal == 'instr') {
                $.ajax({
                    url: 'signal/',
                    data: { 'signal': signal },
                    success: function (res) {
                        stage = 0;
                        update(res);
                    }
                })
            }
            // 执行特定一阶段(fetch, decode, excute, memory, write back, PC update)
            else if (signal == 'stage') {
                $.ajax({
                    url: 'signal/',
                    data: { 'signal': signal },
                    success: function (res) {
                        // BUG: after refreshing page, stage should be zero
                        stage++;
                        if (stage >= 6) stage -= 6;
                        update(res);
                    }
                })
            }
            break;
        }
        default: {
            alert("ALERT: Not Executable!");
        }
    }
}

function prev() {
    $.ajax({
        url: 'last_step/',
        success: function (res) {
            if (res.success) {
                stage = 0;
                update(res);
            } else {
                alert("Last step failed: history record stack is empty")
            }
        }
    })
}

// 重置
function reset() {
    $.ajax({
        url: 'signal/',
        data: { 'signal': 'reset' },
        success: function (res) {
            init();
            $("#code").html(content(code_dict, 0));
            $("#memory").html(content(res, 5))
            code_highlight(res, 'init');
            run_flag = 1;
            last_res = res;
            rsp_init = 0;
        }
    })
}

// 执行完一步后更新
function update(res) {
    $("#register").html(content(res, 1));
    $("#pc").html(content(res, 2));
    $("#cc").html(content(res, 3));
    $("#stat").html(content(res, 4));
    $("#memory").html(content(res, 5));
    $("#stage").html(content(res, 6));
    code_highlight(res, 'next');
    mem_code_set(res);
    mem_frame_set(res);
    $(".changed").css("background-color", "rgb(143,255,203)");

    if (res.ERR != '') {
        alert(res.ERR);
    }
    run_flag = res.STAT;
    last_res = res;
}

// js写入HTML
function content(res, flag) {
    let str;
    switch (flag) {
        case 0: {
            // code table, input=code_dict
            str = '';
            let rows = code_dict.length;
            for (let i = 0; i < rows; i++) {
                let l = code_dict[i];
                str += "<tr> <td>" + l.line + "</td> <td>" + l.text;
            }
            break;
        }
        case 1: {
            // register table
            str = "<tr> <th>Registers</th> <th>Value</th> </tr>";
            for (let i in res.REG) {
                if (last_res.REG[i] != res.REG[i])
                    str += "<tr class='changed'> <td>" + i + "</td> <td>" + full_str(res.REG[i]) + "</td> </tr>";
                else
                    str += "<tr class='unchanged'> <td>" + i + "</td> <td>" + full_str(res.REG[i]) + "</td> </tr>";
            }
            break;
        }
        case 2: {
            // PC table
            str = "<tr> <th>PC</th> </tr>";
            if (last_res.PC != res.PC)
                str += "<tr class='changed'> <td>" + full_str(res.PC, 3) + "</td> </tr>";
            else
                str += "<tr class='unchanged'> <td>" + full_str(res.PC, 3) + "</td> </tr>";
            break;
        }
        case 3: {
            // CC table
            str = "<tr> <th colspan='2'>CC</th> </tr>";
            for (let i in res.CC) {
                if (last_res.CC[i] != res.CC[i])
                    str += "<tr class='changed'> <td>" + i + "</td> <td>" + res.CC[i] + "</td> </tr>";
                else
                    str += "<tr class='unchanged'> <td>" + i + "</td> <td>" + res.CC[i] + "</td> </tr>";
            }
            break;
        }
        case 4: {
            // stat table
            str = "<tr> <th>Stat</th> </tr>";
            if (last_res.STAT != res.STAT)
                str += "<tr class='changed'> <td>" + res.STAT + "</td> </tr>";
            else
                str += "<tr class='unchanged'> <td>" + res.STAT + "</td> </tr>";
            break;
        }
        case 5: {
            // memory table
            // 对于在MEM中的元素，key换为16进制，并按照内存从大到小排序
            str = "<tr> <th>Address</th> <th>Value</th> </tr>";
            let mem_arr = Object.entries(res.MEM);
            let rows = mem_arr.length;

            // memory输出，地址从大到小，给memory table每行添加id: e.g. mem_16
            for (let i = rows - 1; i >= 0; i--) {
                let addr_int = Number(mem_arr[i][0])
                let addr_hex = '0x' + addr_int.toString(16);
                let val = mem_arr[i][1];
                let cls;
                if (last_res.MEM[addr_int] != val)
                    cls = "changed";
                else
                    cls = "unchanged";
                str += "<tr id='mem_" + addr_int + "' class='" + cls + "'> <td>" + full_str(addr_hex, 3) + "</td> <td>" + full_str(val) + "</td> </tr>";
            }
            break;
        }
        case 6: {
            // stage table
            str = "<thead><tr> <th colspan='2'>Next Stage</th> <th colspan='2'>" + STAGE_NAME[stage] + "</th> </tr></thead>" +
                "<tr> <td>rA</td> <td>" + REGISTER_LIST[Number(res.TEMP.rA)] + "</td> " +
                " <td>rB</td> <td>" + REGISTER_LIST[Number(res.TEMP.rB)] + "</td> </tr>" +
                "<tr> <td>valA</td> <td>" + full_str(res.TEMP.valA) + "</td> " +
                " <td>valB</td> <td>" + full_str(res.TEMP.valB) + "</td> " +
                "<tr> <td>valC</td> <td>" + full_str(res.TEMP.valC) + "</td> " +
                " <td>valE</td> <td>" + full_str(res.TEMP.valE) + "</td> </tr>" +
                "<tr> <td>valM</td> <td>" + full_str(res.TEMP.valM) + "</td> " +
                " <td>valP</td> <td>" + full_str(res.TEMP.valP) + "</td> </tr>" +
                "<tr> <td>srcA</td> <td>" + full_str(res.TEMP.srcA) + "</td> " +
                " <td>srcB</td> <td>" + full_str(res.TEMP.srcB) + "</td> </tr>" +
                "<tr> <td>dstE</td> <td>" + full_str(res.TEMP.dstE) + "</td> " +
                " <td>dstM</td> <td>" + full_str(res.TEMP.dstM) + "</td> </tr>";
            break;
        }
        default: str = ''
    }
    return str;
}

function init() {
    // code table
    let str = "<tr> <td></td> </tr>";
    let foo = "<tr> <td></td> </tr>";
    $("#code").html(str + foo + foo + foo + foo + foo + foo + foo + foo + foo);

    // register table
    str = "<tr> <th>Registers</th> <th>Value</th> </tr>";
    let rows = REGISTER_LIST.length - 1
    for (let i = 0; i < rows; i++) {
        str += "<tr> <td>" + REGISTER_LIST[i] + "</td> <td>" + full_str(0) + "</td> </tr>"
    }
    $("#register").html(str);

    // pc table
    str = "<tr> <th>PC</th> </tr>" + "<tr> <td>" + full_str(0, 3) + "</td> </tr>"
    $("#pc").html(str);

    // cc table
    str = "<tr> <th colspan='2'>CC</th> </tr>";
    rows = CC_LIST.length;
    for (let i = 0; i < rows; i++) {
        str += "<tr> <td>" + CC_LIST[i] + "</td> <td>" + 0 + "</td> </tr>"
    }
    $("#cc").html(str);

    // stat table
    str = "<tr> <th>Stat</th> </tr>" + "<tr> <td>" + '/' + "</td> </tr>"
    $("#stat").html(str);

    // memory table
    str = "<tr> <th>Address</th> <th>Value</th> </tr>";
    foo = "<tr> <td></td> <td></td> </tr>";
    $("#memory").html(str + foo + foo + foo + foo + foo + foo + foo + foo + foo);

    // stage
    str = "<tr> <th>Stage</th> </tr>" + "<tr> <td>" + '/' + "</td> </tr>"
    $("#stage").html(str);

}



// 执行过程中code table高亮实现
function code_highlight(res, option) {
    // code table第instr_count行高亮
    var instr_count = next_code(res, option) - 1;
    $("#code tr:even").css("background-color", "rgb(188,221,255)");
    $("#code tr:odd").css("background-color", "rgb(221,238,255)");
    $("#code tr:eq(" + instr_count + ")").css("background-color", "rgba(30, 255, 150, 0.5)");
}

// 得到code table高亮的行
function next_code(res, option = 'next') {
    var instr_count;
    // 下一步的高亮
    if (option == 'next') {
        for (var i in code_dict) {
            var elem = code_dict[i];
            if (parseInt(elem.pc) == res.PC && elem.code != '') {
                instr_count = elem.line;
                break;
            }
        }
    }
    // 初始行
    else if (option == 'init') {
        for (var i in code_dict) {
            var elem = code_dict[i];
            if (elem.pc != '' && elem.code != '') {
                instr_count = elem.line;
                break;
            }
        }
    }
    return instr_count
}



// 给memory代码段添加 code_mem 类
function mem_code_set(res) {
    if (res.rsp_min != 0) {
        for (let i in res.MEM) {
            if (i < Number(res.rsp_min))
                $("#mem_" + i).addClass("code_mem")
        }
    }
    $(".code_mem").css("background-color", "rgb(147,173,255)");
}

// 给memory栈帧添加 frame_mem 类
function mem_frame_set(res) {
    console.log(res.REG.rsp, rsp_init)
    if (rsp_init == 0 && res.REG.rsp != 0)
        rsp_init = res.REG.rsp;
    if (res.REG.rsp < rsp_init) {
        for (let i in res.MEM) {
            if (i >= Number(res.REG.rsp) && i < Number(rsp_init))
                $("#mem_" + i).addClass("frame_mem");
        }
    }
    $(".frame_mem").css("background-color", "rgba(26,255,56,0.772)");
}



// 补齐16进制数字并大写，四位隔开
function full_str(str, len = 16) {
    if (str == null) return '/';
    var substr = String(str).slice(2)
    var num = substr.toUpperCase();
    var num_full = num.padStart(len, 0)
    if (len == 16) {
        let num_sep = num_full.slice(0, 4) + ' ' + num_full.slice(4, 8) + ' '
            + num_full.slice(8, 12) + ' ' + num_full.slice(12, 16)
        return '0x ' + num_sep
    }
    else return '0x ' + num_full
}

