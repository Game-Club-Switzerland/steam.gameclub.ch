(function(){
        function getCurrentScriptSrc() {
        var s = document.currentScript && document.currentScript.src;
        if (!s) {
            var scripts = document.getElementsByTagName('script');
            s = scripts[scripts.length - 1] && scripts[scripts.length - 1].src;
        }
        return s || '';
        }

        function loadWidget(el) {
        var groupId = el.getAttribute('data-group-id');
        if (!groupId) return;
        var widgetUrl = el.getAttribute('data-widget-url');
        if (!widgetUrl) {
            var base = getCurrentScriptSrc().replace(/\/[^\/]*$/, '');
            // default path: /widget/group/{groupID}.html relative to the script location
            widgetUrl = base + '/widget/group/' + encodeURIComponent(groupId) + '.html';
        }

        function fetchAndRender() {
            fetch(widgetUrl, {mode: 'cors'}).then(function(res){
            if (!res.ok) throw new Error('Network response was not ok');
            return res.text();
            }).then(function(html){
            el.innerHTML = html;
            }).catch(function(err){
            console.error('Failed to load Steam group widget:', err);
            });
        }

        // initial load
        fetchAndRender();
        // refresh every 5 minutes
        var FIVE_MIN = 5 * 60 * 1000;
        setInterval(fetchAndRender, FIVE_MIN);
        }

        function init() {
        var els = document.querySelectorAll('.steam-group-widget-embed');
        if (els.length) {
            Array.prototype.forEach.call(els, function(el){ loadWidget(el); });
        }
        }

        if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
        } else {
        init();
        }
    })();