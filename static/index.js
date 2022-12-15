var code_dict;   // 指令code_table的字典
var stage = 0;   // 用于标记单阶段运行，下一阶段为哪一阶段
const STAGE_MAX = 6;
const REGISTER_LIST = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', '/']
const CC_LIST = ['ZF', 'SF', 'OF']
const STAGE_NAME = ['FETCH', 'DECODE', 'EXECUTE', 'MEMORY', 'WRITE BACK', 'PC UPDATE']
var run_flag = false;


function upload(){
    var file = new FormData();
    file.append("file", $("#file")[0].files[0]);
    $.ajax({
        url: 'upload/',
        type: 'post',
        data: file,
        contentType: false,
        processData: false,
        success: function(res){     // response 回调函数
            code_dict = res.code_dict;
            init();
            $("#code").html(content(code_dict, 0));
            $("#memory").html(content(res, 5))
            highlight(res, 'init');
            run_flag = true;
        }
    })
}

// 执行一条指令
function one_instr(){
    if (!run_flag) {
        alert("ALERT: You should upload files first!")
    }
    else {
        $.ajax({
            url: 'signal/',
            data: {'signal': 'instr'},    // signal='instr'：运行一个指令；signal='stage'：运行一个阶段，传参给后端
            success: function(res){
                stage = 0;
                update(res);
            }
        })
    }
}

// 执行特定一阶段(fetch, decode, excute, memory, write back, PC update)
function one_stage(){
    if (!run_flag) {
        alert("ALERT: You should upload files first!")
    }
    else {
        $.ajax({
            url: 'signal/',
            data: {'signal': 'stage'},       // signal='instr'：运行一条指令；signal='stage'：运行一个阶段，传参给后端
            success: function(res){
                stage++;
                if (stage >= 6) stage -= 6;
                update(res);
            }
        })
    }
}

// 重置
function reset(){
    $.ajax({
        url: 'signal/',
        data: {'signal': 'reset'},    // signal='instr'：运行一个指令；signal='stage'：运行一个阶段，传参给后端
        success: function(res){
            init();
            $("#code").html(content(code_dict, 0));
            $("#memory").html(content(res, 5))
            highlight(res, 'init');
        }
    })
}

// 执行完一步后更新
function update(res){
    $("#register").html(content(res, 1));
    $("#pc").html(content(res, 2));
    $("#cc").html(content(res, 3));
    $("#stat").html(content(res, 4));
    $("#memory").html(content(res, 5));
    $("#stage").html(content(res, 6));
    highlight(res, 'next');
    if (res.ERR != ''){
        alert(res.ERR);
    }
}

// js写入HTML
function content(input, flag){
    let str;
    switch (flag){
        case 0: {
            // code table, input=code_dict
            str = '';
            let rows = input.length;
            for (let i = 0; i < rows; i++){
                let l = input[i];
                str += "<tr> <td>" + l.line + "</td> <td>" + l.text;
            }
            break;
        }
        case 1: {
            // register table
            str = "<tr> <th>Registers</th> <th>Value</th> </tr>";
            for (let i in input.REG){
                str += "<tr> <td>" + i + "</td> <td>" + full_str(input.REG[i]) + "</td> </tr>";
            }
            break;
        }
        case 2: {
            // PC table
            str = "<tr> <th>PC</th> </tr>";
            str += "<tr> <td>" + full_str(input.PC, 3) + "</td> </tr>";
            break;
        }
        case 3: {
            // CC table
            str = "<tr> <th colspan='2'>CC</th> </tr>";
            for (let i in input.CC){
                str += "<tr> <td>" + i + "</td> <td>" + input.CC[i] + "</td> </tr>";
            }
            break;
        }
        case 4: {
            // stat table
            str = "<tr> <th>Stat</th> </tr>";
            str += "<tr> <td>" + input.STAT + "</td> </tr>";
            break;
        }
        case 5: {
            // memory table
            // 对于在MEM中的元素，key换为16进制，并按照内存从大到小排序
            str = "<tr> <th>Address</th> <th>Value</th> </tr>";
            let mem_arr = Object.entries(input.MEM);
            let length = mem_arr.length;

            // memory输出
            for (let i = length - 1; i >= 0; i --){
                let addr = '0x' + Number(mem_arr[i][0]).toString(16); 
                let val = mem_arr[i][1];
                str += "<tr> <td>" + full_str(addr, 3) + "</td> <td>" + full_str(val) + "</td> </tr>";
            }


            break;
        }
        case 6: {
            // stage table
            str = "<tr> <th>Stage</th> <th>" + STAGE_NAME[stage] + "</th> </tr>" +
                  "<tr> <td>rA</td> <td>" + REGISTER_LIST[input.TEMP.rA] + "</td> </tr>" +
                  "<tr> <td>rB</td> <td>" + REGISTER_LIST[input.TEMP.rB] + "</td> </tr>" +
                  "<tr> <td>valA</td> <td>" + full_str(input.TEMP.valA) + "</td> </tr>" +
                  "<tr> <td>valB</td> <td>" + full_str(input.TEMP.valB) + "</td> </tr>" +
                  "<tr> <td>valC</td> <td>" + full_str(input.TEMP.valC) + "</td> </tr>" +
                  "<tr> <td>valE</td> <td>" + full_str(input.TEMP.valE) + "</td> </tr>" +
                  "<tr> <td>valM</td> <td>" + full_str(input.TEMP.valM) + "</td> </tr>" +
                  "<tr> <td>valP</td> <td>" + full_str(input.TEMP.valP) + "</td> </tr>";
            break;
        }
        default: str = ''
    }
    return str;
}

function init(){
    // code table
    let str = "<tr> <td></td> </tr>";
    let foo = "<tr> <td></td> </tr>";
    $("#code").html(str + foo + foo + foo + foo + foo + foo + foo + foo + foo);
    
    // register table
    str = "<tr> <th>Registers</th> <th>Value</th> </tr>";
    let length = REGISTER_LIST.length - 1
    for (let i = 0; i < length; i++){
        str += "<tr> <td>" + REGISTER_LIST[i] + "</td> <td>" + full_str(0) + "</td> </tr>"
    }
    $("#register").html(str);

    // pc table
    str = "<tr> <th>PC</th> </tr>" + "<tr> <td>" + full_str(0,3) + "</td> </tr>"
    $("#pc").html(str);
    
    // cc table
    str = "<tr> <th colspan='2'>CC</th> </tr>";
    length = CC_LIST.length
    for (let i = 0; i < length; i++){
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

// 执行过程中高亮实现
function highlight(res, option='next') {
    // code table第instr_count行高亮
    var instr_count = next_code(res, option)
    var tbl = document.getElementById("code");
    sub_highlight(tbl, instr_count - 1)
    
    if (option == 'next'){
        // register table第[line]行高亮
        line = next_register(res);
        tbl = document.getElementById("register");
        sub_highlight(tbl, line);
    }

    // memory table代码段高亮
    line = next_mem(res, option='init')
    tbl = document.getElementById("memory");
    sub_highlight(tbl, line);

}

// 得到code table高亮的行
function next_code(res, option='next'){
    var instr_count;
    // 下一步的高亮
    if (option == 'next'){
        for (var i in code_dict){
            var elem = code_dict[i];
            if (parseInt(elem.pc) == res.PC && elem.code != ''){
                instr_count = elem.line;
                break;
            }
        }
    }
    // 初始行
    else if (option == 'init'){
        for (var i in code_dict){
            var elem = code_dict[i];
            if (elem.pc != '' && elem.code != ''){
                instr_count = elem.line;
                break;
            }
        }
    }
    return instr_count
}

// 得到register table高亮的行
function next_register(res){
    // 若有15，不返回F寄存器
    if (res.TEMP.rA == 15 && res.TEMP.rB == 15) {
        return [];
    }
    else if (res.TEMP.rA != 15 && res.TEMP.rB == 15) {
        return res.TEMP.rA + 1;
    }
    else if (res.TEMP.rA == 15 && res.TEMP.rB != 15) {
        return res.TEMP.rB + 1;
    }
    else 
        return [res.TEMP.rA + 1, res.TEMP.rB + 1];
}

// 得到memory table高亮的行
function next_mem(res, option='next'){
    let mem_arr = Object.entries(res.MEM);
    let rows = mem_arr.length;
    // 代码段高亮
    
        // 标记代码段内存最大处
        let rsp_min = res.TEMP.rsp_min;

        // memory代码段最多延申到code_length处
        let code_length = 0;
        while(1) {
            if (mem_arr[code_length][0] == rsp_min || code_length == rows)
                break;
            else code_length++;
        }

        // 代码段
        line = Array(code_length)
        for (i = 0; i < code_length; i++) {
            line[i] = rows - code_length + i + 1
        }
        return line


}

function sub_highlight(tbl, line, cover=true, color="rgba(30, 255, 150, 0.5)", 
            color1="rgba(30, 144, 255, 0.15)", color2="rgba(30, 144, 255, 0.3)") 
{
    var trs = tbl.getElementsByTagName("tr");
    let rows = trs.length;

    if (cover) {
        for (let i = 0; i < rows; i++) {
            if (i % 2 == 0){
                trs[i].style.background = color2;
            }
            else {
                trs[i].style.background = color1;
            }
        }
    }
    if (typeof(line) == 'number') {
        trs[line].style.background = color;
    }
    else if (typeof(line) == 'object') {
        let length = line.length;
        for (let i = 0; i < length; i++) {
            trs[line[i]].style.background = color;
        }
    }
    return;
}


// 补齐16进制数字并大写，四位隔开
function full_str(str, len=16){
    if (str == null) return '/';
    var substr = String(str).slice(2)
    var num = substr.toUpperCase();
    var num_full = num.padStart(len, 0)
    if (len == 16){
        let num_sep = num_full.slice(0,4) + ' ' + num_full.slice(4,8) + ' '
                    + num_full.slice(8,12) + ' ' + num_full.slice(12,16)
        return '0x ' + num_sep
    }
    else return '0x ' + num_full
}
