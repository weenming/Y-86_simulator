var code_dict;   // 指令code_table的字典
var rows;      // code_dict总行数
const STEP_MAX = 6;
const REGISTER_LIST = ['rax', 'rcx', 'rdx', 'rbx', 'rsp', 'rbp', 'rsi', 'rdi', 'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14']
const CC_LIST = ['ZF', 'SF', 'OF']


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
            $("#code").html(content(code_dict, 0));
            highlight(0, 'init');
        }
    })
}

// 执行一条指令
function one_ins(){
    $.ajax({
        url: 'signal/',
        data: {'signal': 'ins'},    // signal='ins'：运行一句；signal='step'：运行一步，传参给后端
        success: function(res){
            $("#register").html(content(res.REG, 1));
            $("#pc").html(content(res.PC, 2));
            $("#cc").html(content(res.CC, 3));
            $("#stat").html(content(res.STAT, 4));
            $("#memory").html(content(res.MEM, 5));
            highlight(res, 'next');
            if (res.ERR != ''){
                alert(res.ERR);
            }
        }
    })
}

// 执行特定一步(fetch, decode, excute, memory, write back, PC update)
function one_step(){
    $.ajax({
        url: 'signal/',
        data: {'signal': 'step'},       // signal='ins'：运行一句；signal='step'：运行一步，传参给后端
        success: function(res){
            $("#register").html(content(res.REG, 1));
            $("#pc").html(content(res.PC, 2));
            $("#cc").html(content(res.CC, 3));
            $("#stat").html(content(res.STAT, 4));
            $("#memory").html(content(res.MEM, 5));
            highlight(res, 'next');
            if (res.ERR != ''){
                alert(res.ERR);
            }
        }
    })
}

function content(input, flag){
    let str;
    switch (flag){
        case 0: {
            str = "<tr> <th>Line</th> <th>PC</th> <th>Binary Code</th> <th>Text</th> </tr>";
            rows = input.length;
            for (let i = 0; i < rows; i++){
                let l = input[i];
                str += "<tr> <td>" + l.line +"</td> <td>" + l.pc + "</td> <td>" + l.code + "</td> <td>" + l.text + "</td> </tr>"
            }
            return str;
        }
        case 1: str = "<tr> <th>Register Name</th> <th>Register Value</th> </tr>"; break;
        case 2: str = "<tr> <th>PC Value</th> </tr>"; break;
        case 3: str = "<tr> <th>CC Name</th> <th>CC Value</th> </tr>"; break;
        case 4: str = "<tr> <th>Stat Value</th> </tr>"; break;
        case 5: str = "<tr> <th>Memory Address</th> <th>Value</th> </tr>"; break;
        default: str = '';
    }
    if (typeof(input) == 'object'){
        // 对于在MEM中的元素，key换为16进制
        if (flag == 5){
            for (let i in input){
                i_int = Number(i);
                i_hex = '0x' + i_int.toString(16);
                str += "<tr> <td>" + full_str(i_hex, 3) + "</td> <td>" + full_str(input[i]) + "</td> </tr>";
            }
        }
        // 对于REG中的数值，结果换成16进制
        else if (flag == 1){
            for (let i in input){
                str += "<tr> <td>" + i + "</td> <td>" + full_str(input[i]) + "</td> </tr>";
            }
        }
        // CC
        else {
            for (let i in input){
                str += "<tr> <td>" + i + "</td> <td>" + input[i] + "</td> </tr>";
            }
        }
    }
    // PC STAT
    else{
        str += "<tr> <td>" + input + "</td> </tr>";
    }
    return str;
}

function init(){
    let str = "<tr> <th>Line</th> <th>PC</th> <th>Binary Code</th> <th>Text</th> </tr>";
    let foo = "<tr> <td></td> <td></td> <td></td> <td></td> </tr>";
    $("#code").html(str + foo + foo + foo + foo + foo);
    
    str = "<tr> <th>Register Name</th> <th>Register Value</th> </tr>";
    let length = REGISTER_LIST.length
    for (let i = 0; i < length; i++){
        str += "<tr> <td>" + REGISTER_LIST[i] + "</td> <td>" + full_str(0) + "</td> </tr>"
    }
    $("#register").html(str);

    str = "<tr> <th>PC Value</th> </tr>" + "<tr> <td>" + 0 + "</td> </tr>"
    $("#pc").html(str);
    
    str = "<tr> <th>CC Name</th> <th>CC Value</th> </tr>";
    length = CC_LIST.length
    for (let i = 0; i < length; i++){
        str += "<tr> <td>" + CC_LIST[i] + "</td> <td>" + 0 + "</td> </tr>"
    }
    $("#cc").html(str);

    str = "<tr> <th>Stat Value</th> </tr>" + "<tr> <td>" + '/' + "</td> </tr>"
    $("#stat").html(str);

    str = "<tr> <th>Memory Address</th> <th>Value</th> </tr>"
    foo = "<tr> <td></td> <td></td> </tr>";
    $("#memory").html(str + foo + foo + foo + foo + foo);

}

// 执行过程中高亮实现
function highlight(res, option='next') {
    var ins_count;
    // 下一步的高亮
    if (option == 'next'){
        for (var i in code_dict){
            var elem = code_dict[i];
            if (parseInt(elem.pc) == res.PC && elem.code != ''){
                ins_count = elem.line;
                break;
            }
        }
    }
    // 初始化的高亮
    else if (option == 'init'){
        for (var i in code_dict){
            var elem = code_dict[i];
            if (elem.pc != '' && elem.code != ''){
                ins_count = elem.line;
                break;
            }
        }
    }
    
    console.log(ins_count);
    // 代码块第ins_count行高亮
    var tbl = document.getElementById("code");;
    var trs = tbl.getElementsByTagName("tr");
    for (let i = 0; i < rows; i++) {
        trs[i].style.background = "white";
    }
    trs[ins_count].style.background = "yellow";
}

// 补齐16进制数字并大写，四位隔开
function full_str(str, len=16){
    var num = (str.slice(2)).toUpperCase();
    var num_full = num.padStart(len, 0)
    if (len == 16){
        let num_sep = num_full.slice(0,4) + ' ' + num_full.slice(4,8) + ' '
                    + num_full.slice(8,12) + ' ' + num_full.slice(12,16)
        return '0x ' + num_sep
    }
    else return '0x ' + num_full
}