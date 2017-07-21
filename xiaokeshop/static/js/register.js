$(function () {

    var error_name = false;
    var error_password = false;
    var error_check_password = false;
    var error_email = false;
    var error_check = false;

    // 当name表单失去焦点的时候，校验用户名
    $('#name').blur(function () {
        check_user_name();
    });

    $('#pwd').blur(function () {
        check_pwd();
    });

    $('#cpwd').blur(function () {
        check_cpwd();
    });

    $('#email').blur(function () {
        check_email();
    });

    $('#allow').click(function () {
        if ($(this).is(':checked')) {
            error_check = false;
            $(this).siblings('span').hide();
        }
        else {
            error_check = true;
            $(this).siblings('span').html('请勾选同意').show();
        }
    });


    function check_user_name() {
        var len = $('#name').val().length;
        if (len < 5 || len > 20) {
            $('#name').next().html('请输入5-20个字符的用户名').show();
            error_name = true;
        }
        else {
            //这里要判断用户名是否已经注册过
            // 采用post的话需要添加csrf_token的值，给浏览器，django框架中自己做校验
            // 'csrfmiddlewaretoken':$('input:first').val();
            $.get('/user/register_name/', {'get_user_name': $('#name').val()}, function (data) {
                if (data.num >= 1) {
                    //用户名不可用
                    $('#name').next().html('亲！用户名已经存在').show();
                    error_name = true
                } else {
                    // 用户名可用
                    $('#name').next().hide();
                    error_name = false;
                }
            });
        }
    }

    function check_pwd() {
        var len = $('#pwd').val().length;
        if (len < 8 || len > 20) {
            $('#pwd').next().html('密码最少8位，最长20位').show();
            error_password = true;
        }
        else {
            $('#pwd').next().hide();
            error_password = false;
        }
    }


    function check_cpwd() {
        var pass = $('#pwd').val();
        var cpass = $('#cpwd').val();

        if (pass != cpass) {
            $('#cpwd').next().html('两次输入的密码不一致').show();
            error_check_password = true;
        }
        else {
            $('#cpwd').next().hide();
            error_check_password = false;
        }

    }

    function check_email() {
        //邮箱的验证
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

        if (re.test($('#email').val())) {
            $('#email').next().hide();
            error_email = false;
        }
        else {
            $('#email').next().html('你输入的邮箱格式不正确').show();
            error_check_password = true;
        }

    }


    $('#reg_form').submit(function () {
        check_user_name();
        check_pwd();
        check_cpwd();
        check_email();

        if (error_name === false && error_password === false && error_check_password === false && error_email === false && error_check === false) {
            // 返回true，提交表单信息
            return true;
        }
        else {
            //返回false，步提交表单信息
            return false;
        }

    });


});