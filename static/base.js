    function select_plugin(e) {
        console.log('load plugin ' + e.value);

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
            no_focus = false
        }
    }

    function check_focus() {
        webview = document.getElementById('webview');
        var c = webview.childNodes;
        var no_focus = true;
        c.forEach(check_active_element)
        return no_focus;
    }

    function plugin_update() {
        $('#update').load('/plugin/update/');
        if (check_focus()){
            $('#webview').load('/plugin/webview');
        }
    }

    function poll_plugin_update() {
        setTimeout(function(){
            plugin_update();
            poll_plugin_update();
        }, 10000);
    };

    plugin_update();
    poll_plugin_update();
