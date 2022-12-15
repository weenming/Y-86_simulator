var code_dict;   // 指令code_table的字典
var stage = 0;   // 用于标记单阶段运行，下一阶段为哪一阶段
var rsp_init = false;   // 用于标记rsp是否初始化过
const STAGE_MAX = 6;
const REGISTER_LIST = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', '/']
const CC_LIST = ['ZF', 'SF', 'OF']
const STAGE_NAME = ['FETCH', 'DECODE', 'EXECUTE', 'MEMORY', 'WRITE BACK', 'PC UPDATE']


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
            code_dict = res;
            init();
            $("#code").html(content(code_dict, 0));
            highlight(0, 'init');
        }
    })
}

// 执行一条指令
function one_instr(){
    $.ajax({
        url: 'signal/',
        data: {'signal': 'instr'},    // signal='instr'：运行一个指令；signal='stage'：运行一个阶段，传参给后端
        success: function(res){
            stage = 0;
            update(res);
        }
    })
}

// 执行特定一阶段(fetch, decode, excute, memory, write back, PC update)
function one_stage(){
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

// 重置
function reset(){
    $.ajax({
        url: 'signal/',
        data: {'signal': 'reset'},    // signal='instr'：运行一个指令；signal='stage'：运行一个阶段，传参给后端
        success: function(){
            init();
            $("#code").html(content(code_dict, 0));
            highlight(0, 'init');
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
            let rsp = input.REG.rsp;
            let rsp_min = input.TEMP.rsp_min;   // 标记代码段内存最大处
            
            // rsp是否初始化
            if (rsp != '0x0' && rsp_init == false) {
                rsp_init = true
            }
            
            // memory代码段最多延申到code_length处
            let code_length = 0;
            while(1) {
                if (mem_arr[code_length][0] == rsp_min || code_length == length)
                    break;
                else code_length++;
            }

            console.log(rsp);
            console.log(rsp_min);
            console.log(mem_arr[code_length][0])
            
            // memory代码段输出
            for (let i = code_length - 1; i >= 0; i --){
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
    let str = "<tr> <th></th> </tr>";
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
    sub_highlight(tbl, instr_count - 1);
    
    if (option == 'next'){
            // register table第[line]行高亮
    line = next_register(res);
    tbl = document.getElementById("register");
    sub_highlight(tbl, line);
    }
}

// 得到code table高亮的行数
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

// 得到register table高亮的行数
function next_register(res){
    // console.log(res.TEMP.rA)
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

function sub_highlight(tbl, line) {
    var trs = tbl.getElementsByTagName("tr");
    let rows = trs.length;
    // console.log(rows);
    // console.log(line);
    for (let i = 0; i < rows; i++) {
        trs[i].style.background = "white";
    }
    if (typeof(line) == 'number') {
        trs[line].style.background = "yellow";
    }
    else if (typeof(line) == 'object') {
        let length = line.length;
        for (let i = 0; i < length; i++) {
            trs[line[i]].style.background = "yellow";
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
