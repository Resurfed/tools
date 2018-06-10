$(document).ready(function () {

    // Web socket stuff
    const ws = new channels.WebSocketBridge();
    ws.connect('/ws/uploader');
    let log = $(".ui.bulleted.list");


    function add_log_message(message) {
        log.append('<div class="item">' + message + '</div>')
    }

    function add_log_list(node_id, message) {
        let i = '<div class="item">'
                + '<div>' + message + '</div>'
                + '<div id="list_' + node_id + '" class="ui list"></div>'
            + '</div>';
        log.append(i)
    }

    function add_log_sub_item(node_id, message) {
        let node = 'list_' + node_id;
        let item = '<div class="item">' + message + '</div>';

        $("#" + node).append(item);
    }

    function add_log_sub_list(parent_id, node_id, message) {
        let i = '<div class="item">'
                + '<div>' + message + '</div>'
                + '<div id="list_' + node_id + '" class="ui list"></div>'
            + '</div>';
        let parent_node = 'list_' + parent_id;

        $("#" + parent_node).append(i);
    }

    ws.socket.addEventListener('open', function (event) {
        $(".form").removeClass("loading");
        add_log_message('Connected to uploader backend');
    });

    ws.socket.addEventListener('close', function (evemt) {
        $(".form").addClass("loading");
        // add_log_item('Disconnected from uploader backend');
    });

    ws.socket.addEventListener('message', function (message) {
        console.log(message);
        let packet = JSON.parse(message.data);
        switch (packet.action) {
            case "STARTED TASK":
                add_log_message('Upload task started');
                break;
            case "GENERAL ERROR":
                add_log_message(packet.error);
                break;
            case "PROGRESS UPDATE":
                $("#pbMain").progress('set progress', packet.progress);
                break;
            case "MESSAGE":
                add_log_message(packet.message);
                break;
            case "LIST":
                add_log_list(packet.id, packet.message);
                break;
            case "SUB ITEM":
                add_log_sub_item(packet.id, packet.message);
                break;

            case "SUB LIST":
                add_log_sub_list(packet.parent, packet.id, packet.message);
                break;
        }
    });


    //Main Progress Bar
    $("#pbMain").progress({
        percent: 0
    });

    // Insert map info toggle
    $("#id_insert_map_info").click(function () {
        let map_type = $("#id_map_type");

        $("#map_info :input").attr("disabled", !this.checked);

        map_type.parent().toggleClass("disabled", !this.checked);

    });

    //File input
    $('.inputfile').each(function () {
        let $input = $(this),
            $label = $input.next('label'),
            labelVal = $label.html();

        $input.on('change', function (e) {
            let fileName = e.target.value.split('\\').pop();

            if (fileName)
                $label.find('span').html(fileName);
            else
                $label.html(labelVal);
        });
    });

    function upload_map() {
        let fd = new FormData();

        $.each($('.form').serializeArray(), function (key, input) {
            if (input.value.length === 0)
                return;
            fd.append(input.name, input.value);
        });

        fd.append("map_file", $("#id_map_file")[0].files[0]);

        $.ajax({
            xhr: function () {
                let xhrobj = $.ajaxSettings.xhr();
                if (xhrobj.upload) {
                    xhrobj.upload.addEventListener("progress", function (event) {
                        let percent = 0;
                        let position = event.loaded || event.position;
                        let total = event.total;

                        if (event.lengthComputable) {
                            percent = Math.ceil(position / total * 100);
                        }

                        $("#pbMain").progress('set progress', percent);

                    }, false)
                }
                return xhrobj;
            },
            url: '/uploader/',
            method: "POST",
            contentType: false,
            processData: false,
            cache: false,
            data: fd,
            dataType: 'json',
            success: function (response) {

            }
        });
    }

    $('.form')
        .form({
            keyboardShortcuts: true,
            fields: {
                map_author: {
                    rules: [
                        {
                            type: 'empty'
                        },
                        {
                            type: 'maxLength[32]'
                        }
                    ]
                },
                servers: {
                    rules: [
                        {
                            type: 'empty'
                        }
                    ]
                },
                map_file: {
                    rules: [
                        {
                            type: 'empty'
                        }
                    ]
                },
                map_spawns: {
                    rules: [
                        {
                            type: 'spawns',
                            prompt: "Spawn info is incorrectly formatted"
                        }
                    ]
                }

            },
            onSuccess(event, fields) {
                event.preventDefault();
                upload_map();
            }
        });

});