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