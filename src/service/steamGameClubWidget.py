import os
class SteamGameClubWidget:
    @staticmethod
    def steamGroupWidgetHtml(steamGroup):
        html = f"""<div class="steam-group-widget" style="background: #171a21; color: #c7d5e0; border-radius: 4px; padding: 16px; font-family: 'Motiva Sans', Arial, Helvetica, sans-serif; max-width: 350px; box-sizing: border-box; width: 100%;">
        <style>
        @media (max-width: 480px) {{
            .steam-group-widget {{
                padding: 10px;
                max-width: 100vw;
                font-size: 16px;
            }}
            .steam-group-widget h3 {{
                font-size: 18px !important;
            }}
            .steam-group-widget img {{
                width: 24px !important;
                height: 24px !important;
                margin-right: 6px !important;
            }}
        }}
        </style>
        <h3 style="margin: 0 0 10px 0; font-size: 20px; font-weight: 700;">
            <a href="https://steamcommunity.com/groups/{steamGroup['groupURL']}" style="color: #66c0f4; text-decoration: none;">
                <img src="{steamGroup['avatarIcon']}" alt="{steamGroup['groupName']} Avatar" style="vertical-align: middle; border-radius: 2px; margin-right: 8px; width: 32px; height: 32px;" />
                {steamGroup['groupName']}
            </a>
        </h3>
        <div style="margin-bottom: 4px;">
            <span style="color: #66c0f4; font-weight: 500;">{steamGroup['memberCount']} Mitglieder insgesamt</span>
        </div>
        <div style="margin-bottom: 4px;">
            <span style="color: #c7d5e0;">{steamGroup['memberOnline']} online</span>
        </div>
        <div style="margin-bottom: 4px;">
            <span style="color: #59bf40;">{steamGroup['memberInGame']} im Spiel</span>
        </div>
        <div>
            <span style="color: #c7d5e0;">{steamGroup['memberInChat']} im Chat - 
                <a href="https://steamcommunity.com/chat/invite/IQhgcbIe" style="color: #66c0f4; text-decoration: underline;">Chat beitreten</a>
            </span>
        </div>
        <div style="height:16px;"></div>
    </div>"""
        return html
    
    @staticmethod
    def steamGroupWidget(steamGroup):
        html = SteamGameClubWidget.steamGroupWidgetHtml(steamGroup)
        # Ensure the directory exists
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group/')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{steamGroup['groupID64']}.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return html
    
    @staticmethod
    def steamGroupWidgetOld(steamGroup):
        html = f"""<div class="steam-group-widget" style="background: #171a21; color: #c7d5e0; border-radius: 4px; padding: 16px; font-family: 'Motiva Sans', Arial, Helvetica, sans-serif; max-width: 350px; box-sizing: border-box; width: 100%;">
    <style>
    @media (max-width: 480px) {{
        .steam-group-widget {{
            padding: 10px;
            max-width: 100vw;
            font-size: 16px;
        }}
        .steam-group-widget h3 {{
            font-size: 18px !important;
        }}
        .steam-group-widget img {{
            width: 24px !important;
            height: 24px !important;
            margin-right: 6px !important;
        }}
    }}
    </style>
    <h3 style="margin: 0 0 10px 0; font-size: 20px; font-weight: 700;">
        <a href="https://steamcommunity.com/groups/{steamGroup['groupURL']}" style="color: #66c0f4; text-decoration: none;">
            <img src="{steamGroup['avatarIcon']}" alt="{steamGroup['groupName']} Avatar" style="vertical-align: middle; border-radius: 2px; margin-right: 8px; width: 32px; height: 32px;" />
            {steamGroup['groupName']}
        </a>
    </h3>
    <div style="margin-bottom: 4px;">
        <span style="color: #66c0f4; font-weight: 500;">{steamGroup['memberCount']} Mitglieder insgesamt</span>
    </div>
    <div style="margin-bottom: 4px;">
        <span style="color: #c7d5e0;">{steamGroup['memberOnline']} online</span>
    </div>
    <div style="margin-bottom: 4px;">
        <span style="color: #59bf40;">{steamGroup['memberInGame']} im Spiel</span>
    </div>
    <div>
        <span style="color: #c7d5e0;">{steamGroup['memberInChat']} im Chat - 
            <a href="https://steamcommunity.com/chat/invite/IQhgcbIe" style="color: #66c0f4; text-decoration: underline;">Chat beitreten</a>
        </span>
    </div>
    <div style="height:16px;"></div>
</div>"""
        return html
    
    @staticmethod
    def createJavaScriptFileforImport(steamGroup):
        groupID = steamGroup['groupID64']
        # Create a small JS file that can be embedded on external sites.
        # It looks for elements with class "steam-group-widget-embed" and a data-group-id attribute.
        # Optionally set data-widget-url on the element to point to a custom widget HTML URL.
        js = """(function(){
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
            var base = getCurrentScriptSrc().replace(/\\/[^\\/]*$/, '');
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
    })();"""

        # Ensure the directory exists and write the JS file
        output_dir = os.path.join(os.path.dirname(__file__), '../../docs/widget/group/'+groupID+'/')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'steamGroupWidget.js')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js)
        return js