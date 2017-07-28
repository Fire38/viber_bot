$( document ).ready(function()
{       // добавление и удаление групп/предметов/преподавателей
        $('#add_button').bind('click', function()
        {
            var value = $('#id_name').val();
            var form = $(this).closest('form');
            var name = form.attr('name');
            console.log(name)

            $.ajax(
            {
                url: form.attr('ajax_url'),
                type: "POST",
                data: {
                    'value':value,
                    'type': 'add',
                    'name': name
                },
                dataType: 'json',
                success: function (data)
                {
                    if (data.created)
                    {
                        $('#table_elements').append(data.html);
                    }
                    else
                    {
                        $('#id_name').append('Ошибка');
                        alert('Такое значение уже существует');
                    }
                }
            });
        });

        $('#delete').bind('click', function()
        {
            var form = $(this).closest('form');
            var name = form.attr('name');
            var idForRemove = $('input[name="check"]:checked').map(function()
            {
                return $(this).attr('value');
            }).get();

            var delete_info = window.confirm("При удалении элемента также будут удалены пары, в которых он содержится");
            if (delete_info == true)
            {
                $.ajax(
                {
                    url: form.attr('ajax_url'),
                    type: "POST",
                    data: {
                        'id': idForRemove,
                        'type': 'delete',
                        'name': name
                    },
                    dataType: 'json',
                    success: function ()
                    {
                        $('tr').has('input[name="check"]:checked').remove();
                    }
                });
            }
            else
            {
                alert("Удаление отменено");
            }

        });

        // удаление пар по фильтру
        $('#filter_delete').bind('click', function()
        {
            var form = $(this).closest('form')
            var idForRemove = $('input[name="check"]:checked').map(function(){
                return $(this).attr('value');
            }).get();
            //console.log(idForRemove.length)
            $.ajax(
            {
                url:form.attr('ajax_url'),
                data:{
                    'id': idForRemove,
                    'type': 'delete'
                },
                dataType: 'json',
                success: function()
                {console.log('НАЙдено-', $('tr').has('input[id="check"]:checked').length);
                   $('tr').has('input[id="check"]:checked').remove();
                }

            });
        });

        // выбор всех элементов для удаления
        $('#check_all').bind('click', function(){
            if (this.checked){
                $('input[name=check]').prop('checked', true);
            }
            else{
                $('input[name=check]').prop('checked', false);
            }
        });

        //исчезновение записи о том, что расписание добавлено
        $('#information').fadeOut(4000);
        $('#alert').fadeOut(4000);

        //добавить преподавателя/предмет/группу со страницы расписания
        // появление инпута для добавления
        $('#add_subject').bind('click', function(){
            $(this).hide(200);
            $("#subject_form").show(1000).css({"display":"inline"});
        });

        $('#add_teacher').bind('click', function(){
            $(this).hide(200);
            $("#teacher_form").show(1000).css("display","inline");
        });

        $('#add_group').bind('click', function(){
            $(this).hide(200);
            $("#group_form").show(1000).css("display","inline");
        });

        $('.schedule_add_button').bind('click', function(){
            var value = $(this).prev('input').val();
            var name = $(this).closest('div').attr('name');
            // div - предыдущий div который понадобится для поиска в success
            var div = $(this).closest('div').prev('div');
            $(this).prev('input').val('');

            $.ajax(
            {
                url: '/web_interface/ajax/add/',

                type: "POST",
                data: {
                    'value':value,
                    'type': 'dynamic_add',
                    'name': name
                },
                dataType: 'json',
                success: function (data)
                {
                    if (data.created)
                    {
                        // вот и понадобился
                        div.find('select').append(data.html);
                    }
                }
            });
        });
});

