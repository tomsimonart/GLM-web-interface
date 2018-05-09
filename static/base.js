    function select_plugin(e) {
        $.ajax({
            url: '/plugin/' + e.value,
            method: 'GET',
            error: function(xhr, status, err) {
                console.log(xhr, status, err.toString());
            }
        });

        document.getElementById('update').innerHTML = 0;
        $('#webview').load('/plugin/webview');
    };

    function focus_webview(webview){
        webview.style["background"] = 'linear-gradient(salmon, #e23e5f)';
    }

    function unfocus_webview(webview){
        webview.style["background"] = 'linear-gradient(salmon, crimson)';
    }


    function check_active_element(item, index) {
        if (item === document.activeElement){
            no_focus = false;
        }
    }

    function check_focus() {
        webview = document.getElementById('webview');
        c = webview.childNodes;
        no_focus = true;
        c.forEach(check_active_element);
        return no_focus
    }

    function plugin_update() {
        old_update = new_update;
        $('#update').load('/plugin/update/');
        new_update = Number(document.getElementById('update').innerHTML);
        console.log(old_update + ' ' + new_update);
        if (check_focus()){
            if (old_update < new_update) {
                $('#webview').load('/plugin/webview');
            }
        }
    }

    function poll_plugin_update() {
        setTimeout(function(){
            plugin_update();
            poll_plugin_update();
        }, 5000);
    };

    new_update = 0;
    $('#webview').load('/plugin/webview');
    poll_plugin_update();
