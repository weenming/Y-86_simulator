var code_dict;   // 指令code_table的字典
var ins_dict;    // 运行一句的字典
var step_dict;   // 运行一步的字典
var rows;      // code_dict总行数
var ins_count = 0;
var step_count = 0;
var signal;      // signal='ins'：运行一句；signal='step'：运行一步，传参给后端
const STEP_MAX = 5;
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
        }
    })
}

function one_ins(){
    step_count = 0;
    signal = 'ins';
    while (!code_dict[ins_count].flag) ins_count++;
    ins_count++;
    $.ajax({
        url: 'signal/',
        // type: 'post',
        data: {'signal': signal},
        // contentType: false,
        // processData: false,
        success: function(res){
            ins_dict = res
            $("#register").html(content(ins_dict.REG, 1));
            $("#pc").html(content(ins_dict.PC, 2));
            $("#cc").html(content(ins_dict.CC, 3));
            $("#stat").html(content(ins_dict.STAT, 4));
            $("#memory").html(content(ins_dict.MEM, 5));
        }
    })
}

function one_step(){
    step_count++;
    signal = 'step';
    if (step_count == STEP_MAX) {
        step_count = 0;
        while (!code_dict[ins_count].flag) ins_count++;
        ins_count++;
    }
    $.ajax({
        url: 'signal/',
        data: {'signal': signal},
        success: function(res){
            step_dict = res
            // console.log('res ' + res + ' ins_count ' + ins_count + ' step_count ' + step_count)
        }
    })
}

function content(input, flag){
    let str;
    switch (flag){
        case 0: {
            str = "<tr> <th>Line</th> <th>PC</th> <th>Binary Code</th> <th>Text</th> </tr>";
            var rows = input.length;
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
        for (let i in input){
            str += "<tr> <td>" + i + "</td> <td>" + input[i] + "</td> </tr>";
        }
    }
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
        str += "<tr> <td>" + REGISTER_LIST[i] + "</td> <td>" + 0 + "</td> </tr>"
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
