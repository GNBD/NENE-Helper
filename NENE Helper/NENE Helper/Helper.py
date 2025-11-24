import eel
import sys
import os
import subprocess
import threading
import requests
import re
import shutil
import json
import datetime
import time
import psutil
import zipfile
import webbrowser 
from PIL import Image, ImageDraw
import pystray

eel.init('web')

# 전역 변수
DEFAULT_JAVA = "java"
BASE_SERVERS_DIR = "servers"
LAUNCHER_CONFIG_FILE = "launcher_config.json"
LANG_DIR = "languages"

active_processes = {}
server_logs = {}
current_view_server = None 
server_players = {}
last_backup_times = {}

# [기본 언어 데이터]
DEFAULT_TRANSLATIONS = {
    "ko": {
        "title_launcher": "SERVER<br>LAUNCHER", "btn_new_server": "새 서버", "msg_select_server": "서버를 선택하세요",
        "tab_dashboard": "대시보드", "tab_env": "서버 관리", "tab_players": "플레이어 관리", "tab_broadcast": "📢 광고/공지", "tab_settings": "전체 설정", "tab_info": "ℹ️ 서버 정보", "tab_danger": "⛔ 위험 구간",
        "card_player": "Player", "card_status": "Status", "ph_cmd_input": "명령어 입력...", "btn_start": "서버 시작", "btn_stop": "서버 종료", "btn_restart": "재시작",
        "title_time": "⏰ 시간 제어", "env_morning": "아침", "env_noon": "점심", "env_evening": "저녁", "env_night": "밤",
        "title_weather": "🌥️ 날씨 제어", "env_clear": "맑음", "env_rain": "비", "env_thunder": "폭풍우", "env_lock": "날씨 고정",
        "title_player_list": "접속자 목록", "btn_whitelist": "화이트리스트 관리", "btn_banlist": "차단 목록 관리", "btn_ip_banlist": "IP 차단 관리", "msg_no_players": "접속 중인 플레이어가 없습니다.",
        "title_broadcast": "📢 광고 / 공지 보내기", "desc_broadcast": "서버에 접속한 모든 플레이어에게 메시지를 띄웁니다.",
        "lbl_bc_title": "🖥️ 화면 중앙 타이틀 (Title)", "desc_bc_title": "가장 크게 보이는 제목입니다.",
        "lbl_bc_subtitle": "📝 서브 타이틀 (Subtitle)", "desc_bc_subtitle": "타이틀 아래에 작게 나오는 설명입니다. (타이틀과 함께 보낼 때 사용)",
        "lbl_bc_actionbar": "💬 액션 바 (Actionbar)", "desc_bc_actionbar": "아이템 슬롯 위에 작게 뜨는 메시지입니다.",
        "btn_bc_send": "보내기 (Send)", "btn_bc_set": "설정 (Set)", "btn_bc_clear": "지우기",
        "btn_save_settings": "💾 설정 저장하기", "title_backup": "💾 백업 설정", "set_auto_backup": "자동 백업 활성화", "set_backup_interval": "백업 주기 (분)",
        "btn_backup_now": "지금 백업하기", "title_java": "☕ Java 설정", "set_java_path": "실행 경로 (java.exe)", "msg_java_tip": "* 1.18 이상은 Java 17+, 그 이하는 Java 8 권장",
        "title_general": "📝 일반 설정", "set_motd": "서버 이름 (MOTD)", "set_server_port": "서버 포트", "set_server_ip": "서버 IP", "set_max_players": "최대 인원",
        "set_online_mode": "정품 인증 (Online Mode)", "set_white_list": "화이트리스트 사용", "set_enforce_whitelist": "화이트리스트 강제",
        "title_performance": "🚀 성능 및 네트워크", "set_ram": "메모리 할당", "set_view_distance": "시야 거리", "set_simulation_distance": "연산 거리",
        "set_max_tick_time": "최대 틱 시간", "set_network_compression_threshold": "네트워크 압축 임계값", "set_rate_limit": "패킷 제한",
        "set_use_native_transport": "네이티브 전송 사용", "set_enable_status": "상태 표시 활성화", "set_broadcast_rcon_to_ops": "RCON 로그 방송", "set_broadcast_console_to_ops": "콘솔 로그 방송",
        "title_world": "🌍 월드 및 생성", "set_level_name": "월드 폴더명", "set_level_seed": "월드 시드", "set_level_type": "월드 타입", "set_generator_settings": "생성기 설정",
        "set_max_world_size": "월드 최대 크기", "set_allow_nether": "네더(지옥) 허용", "set_generate_structures": "구조물 생성",
        "title_gameplay": "🎮 게임 플레이", "set_gamemode": "기본 게임모드", "set_force_gamemode": "게임모드 강제", "set_difficulty": "난이도",
        "set_hardcore": "하드코어", "set_pvp": "PVP 허용", "set_allow_flight": "비행 허용", "set_spawn_monsters": "몬스터 스폰", "set_spawn_animals": "동물 스폰",
        "set_spawn_npcs": "NPC 스폰", "set_spawn_protection": "스폰 보호 구역", "set_enable_command_block": "커맨드 블록 허용", "set_player_idle_timeout": "잠수 추방 시간 (분)",
        "title_security": "🔒 보안 및 기타", "set_op_permission_level": "OP 권한 레벨", "set_log_ips": "IP 기록", "set_enforce_secure_profile": "보안 프로필 강제",
        "set_prevent_proxy_connections": "프록시 연결 방지", "set_resource_pack": "리소스팩 URL", "set_require_resource_pack": "리소스팩 강제",
        "set_enable_rcon": "RCON 활성화", "set_rcon_port": "RCON 포트", "set_rcon_password": "RCON 비밀번호", "set_enable_query": "Query 활성화", "set_query_port": "Query 포트",
        "set_sync_chunk_writes": "청크 동기화 저장", "set_enable_jmx_monitoring": "JMX 모니터링", "set_entity_broadcast_range_percentage": "엔티티 방송 범위(%)",
        "set_max_chained_neighbor_updates": "최대 이웃 업데이트", "set_region_file_compression": "청크 압축 방식", "set_accepts_transfers": "서버 이동 허용",
        "set_bug_report_link": "버그 리포트 링크", "set_initial_enabled_packs": "초기 활성 팩", "set_initial_disabled_packs": "초기 비활성 팩", "set_debug": "디버그 모드",
        "title_folder_check": "📂 파일 위치 확인", "desc_folder_check": "서버 파일이나 백업 파일이 저장된 실제 폴더를 엽니다.", "btn_open_server_folder": "📂 서버 폴더 열기", "btn_open_backup_folder": "💾 백업 폴더 열기",
        "title_danger": "🚫 서버 삭제 (Danger Zone)", "msg_danger": "현재 서버를 영구 삭제합니다. 복구할 수 없습니다.", "btn_delete_server": "🗑️ 서버 영구 삭제",
        "modal_p_join": "접속 시간", "modal_p_status": "상태", "btn_whisper": "💬 귓속말 (Whisper)", "btn_tp": "🚀 이동 (TP)",
        "act_op": "관리자 (OP)", "act_deop": "권한 해제 (DEOP)", "act_kick": "추방 (KICK)", "act_ban": "차단 (BAN)", "btn_close": "닫기",
        "modal_whisper_title": "💬 귓속말 보내기", "modal_tp_title": "🚀 텔레포트 (TP)", "msg_tp_ask": "누구에게 이동하시겠습니까?", "msg_tp_empty": "이동할 상대가 없습니다.",
        "modal_ban_opt_title": "🚫 차단 옵션 선택", "msg_ban_opt": "어떤 방식으로 차단하시겠습니까?", "btn_ban_name": "닉네임 차단 (Name Ban)", "btn_ban_ip": "IP 차단 (IP Ban)", "btn_ban_both": "둘 다 차단 (Both)",
        "btn_cancel": "취소", "btn_confirm": "확인", "btn_create": "생성", "btn_save": "저장", "btn_delete": "제거", "btn_add": "추가",
        "modal_confirm_title": "⚠️ 실행 확인", "modal_list_title": "목록 관리", "ph_nickname": "닉네임 / IP 입력",
        "modal_new_title": "✨ 새 서버 생성", "modal_new_name": "서버 이름", "modal_new_ver": "버전", "modal_setting_title": "⚙️ 런처 설정", "modal_setting_lang": "언어 (Language)", "modal_setting_mirror": "미러 URL",
        "modal_del_title": "🚫 정말 삭제하시겠습니까?", "modal_del_msg": "선택된 서버: ", "modal_eula_title": "⚖️ EULA 동의", "msg_eula_content": "마인크래프트 서버를 생성하려면<br>Mojang의 EULA(최종 사용자 라이선스 계약)에<br>동의해야 합니다.",
        "btn_agree": "동의합니다", "btn_disagree": "거절", "msg_cannot_close": "⚠️ 서버가 실행 중입니다! 먼저 서버를 종료해주세요.",
        "diff_peaceful": "평화로움", "diff_easy": "쉬움", "diff_normal": "보통", "diff_hard": "어려움",
        "modal_restart_title": "🔄 서버 재시작 확인", "msg_restart_confirm": "정말 서버를 다시 시작하시겠습니까?<br>(종료 후 다시 시작됩니다)",
        "title_server_info": "ℹ️ 서버 정보", "info_created": "생성 일자", "info_source": "다운로드 출처", "info_size": "디스크 사용량", "info_java": "Java 버전/경로", "info_players": "방문한 플레이어 수"
    },
    "en": { "title_launcher": "SERVER<br>LAUNCHER" } 
}

# ==========================================================
# [기능] 시스템 초기화
# ==========================================================
@eel.expose
def init_system_py():
    if not os.path.exists(BASE_SERVERS_DIR): os.makedirs(BASE_SERVERS_DIR)
    if not os.path.exists(LAUNCHER_CONFIG_FILE):
        with open(LAUNCHER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"language": "ko", "mirror_url": "https://api.papermc.io/v2/projects/paper"}, f, indent=4)
    if not os.path.exists(LANG_DIR): os.makedirs(LANG_DIR)
    
    # [추가] 글로벌 자바 설정 로드
    load_global_java_setting()
    
    for lang_code, default_data in DEFAULT_TRANSLATIONS.items():
        lang_file = os.path.join(LANG_DIR, f"{lang_code}.json")
        final_data = default_data.copy()
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    final_data.update(existing_data)
                    for k, v in default_data.items():
                        if k not in final_data: final_data[k] = v
            except: pass
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

@eel.expose
def get_launcher_config_py():
    if os.path.exists(LAUNCHER_CONFIG_FILE):
        try:
            with open(LAUNCHER_CONFIG_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except: pass
    return {"language": "ko", "mirror_url": "https://api.papermc.io/v2/projects/paper"}

@eel.expose
def save_launcher_config_py(data):
    try:
        # 기존 설정 유지하면서 병합
        current = {}
        if os.path.exists(LAUNCHER_CONFIG_FILE):
            with open(LAUNCHER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                current = json.load(f)
        
        current.update(data)
        
        with open(LAUNCHER_CONFIG_FILE, 'w', encoding='utf-8') as f: json.dump(current, f, indent=4)
        return "✅ 저장 완료"
    except: return "❌ 실패"

@eel.expose
def get_translation_py(lang_code):
    file_path = os.path.join(LANG_DIR, f"{lang_code}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f: return json.load(f)
        except: pass
    return DEFAULT_TRANSLATIONS.get(lang_code, {})

@eel.expose
def get_current_server_py():
    return current_view_server

@eel.expose
def try_close_app_py():
    for name, p in active_processes.items():
        if p.poll() is None:
            return "blocked"
    return "ok"

# ==========================================================
# [기능] 서버 관련
# ==========================================================
@eel.expose
def get_server_list_py():
    if not os.path.exists(BASE_SERVERS_DIR): os.makedirs(BASE_SERVERS_DIR)
    server_list = []
    try:
        for name in os.listdir(BASE_SERVERS_DIR):
            full_path = os.path.join(BASE_SERVERS_DIR, name)
            if os.path.isdir(full_path):
                status = "Ready"
                if name in active_processes and active_processes[name].poll() is None: status = "Running"
                version = ""
                try:
                    config_path = os.path.join(full_path, "nene_config.json")
                    if os.path.exists(config_path):
                        with open(config_path, 'r', encoding='utf-8') as f: version = json.load(f).get("version", "")
                except: pass
                server_list.append({"name": name, "status": status, "version": version})
    except: pass
    return server_list

@eel.expose
def select_server_py(server_name):
    global current_view_server
    current_view_server = server_name
    if server_name in server_logs: eel.restore_logs_js(server_logs[server_name][-1000:])()
    else: eel.restore_logs_js([])()
    is_running = False
    if server_name in active_processes and active_processes[server_name].poll() is None: is_running = True
    eel.update_status_js(is_running)
    update_ui_player_list(server_name)
    return f"Load: {server_name}"

@eel.expose
def get_papermc_versions():
    try:
        mirror_url = "https://api.papermc.io/v2/projects/paper"
        if os.path.exists(LAUNCHER_CONFIG_FILE):
            with open(LAUNCHER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                conf = json.load(f)
                mirror_url = conf.get("mirror_url", mirror_url).strip().rstrip('/')

        headers = {'User-Agent': 'Mozilla/5.0'}
        
        if "purpurmc.org" in mirror_url:
            r = requests.get(mirror_url, headers=headers, timeout=3)
            if r.status_code == 200:
                return r.json().get("versions", [])[::-1]
        else:
            r = requests.get(mirror_url, headers=headers, timeout=3)
            if r.status_code == 200:
                return r.json().get("versions", [])[::-1]

    except: pass
    return ["1.21.4", "1.21.3", "1.21.1", "1.20.4", "1.16.5", "1.12.2"]

@eel.expose
def get_manage_list_py(file_type):
    if not current_view_server: return []
    filename = "whitelist.json"
    if file_type == "banlist": filename = "banned-players.json"
    elif file_type == "ip-banlist": filename = "banned-ips.json"
    path = os.path.join(BASE_SERVERS_DIR, current_view_server, filename)
    res = []
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for i in data:
                    if file_type == "ip-banlist":
                        if "ip" in i: res.append(i["ip"])
                    else:
                        if "name" in i: res.append(i["name"])
        except: pass
    return res

@eel.expose
def get_player_detail_py(player_name):
    if not current_view_server: return None
    info = { "name": player_name, "join_time": "-", "uuid": "-" }
    if current_view_server in server_players and player_name in server_players[current_view_server]:
        info.update(server_players[current_view_server][player_name])
    return info

@eel.expose
def execute_command_py(cmd):
    send_command_py(cmd)
    return f"Cmd: {cmd}"

@eel.expose
def create_new_server_real(server_name, version, mirror_url):
    clean = re.sub(r'[<>:"/\\|?*]', '', server_name).strip()
    if not clean: return "❌ Name Error"
    target = os.path.join(BASE_SERVERS_DIR, clean)
    if os.path.exists(target): return "⚠️ Exists"
    
    try:
        os.makedirs(target)
        headers = {'User-Agent': 'Mozilla/5.0'}
        base = mirror_url.strip().rstrip('/') if mirror_url else "https://api.papermc.io/v2/projects/paper"
        
        eel.update_download_progress_js("Checking API...")()
        
        download_url = ""
        file_name = "server.jar"

        if "purpurmc.org" in base:
            r = requests.get(f"{base}/{version}", headers=headers)
            data = r.json()
            latest_build = data['builds']['latest']
            download_url = f"{base}/{version}/{latest_build}/download"
            file_name = f"purpur-{version}-{latest_build}.jar"
        else:
            r = requests.get(f"{base}/versions/{version}", headers=headers)
            data = r.json()
            latest_build = data['builds'][-1]
            r2 = requests.get(f"{base}/versions/{version}/builds/{latest_build}", headers=headers)
            build_data = r2.json()
            actual_filename = build_data['downloads']['application']['name']
            download_url = f"{base}/versions/{version}/builds/{latest_build}/downloads/{actual_filename}"
            file_name = actual_filename

        eel.update_download_progress_js("Downloading...")()
        
        with requests.get(download_url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(os.path.join(target, "server.jar"), 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
                    
        with open(os.path.join(target, "eula.txt"), 'w') as f: f.write("eula=true")
        
        # [수정됨] 생성일, 출처 정보 추가 저장
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(os.path.join(target, "nene_config.json"), 'w', encoding='utf-8') as f: 
            json.dump({
                "java_path": "java", 
                "version": version, 
                "auto_backup": False, 
                "backup_interval": 60,
                "original_jar": file_name,
                "created_at": now_str,
                "download_source": base
            }, f, indent=4)
            
        return "✅ Done"
        
    except Exception as e:
        if os.path.exists(target): shutil.rmtree(target)
        return f"❌ Error: {e}"

@eel.expose
def delete_server_real(name):
    if name in active_processes: return "⚠️ Running"
    try:
        shutil.rmtree(os.path.join(BASE_SERVERS_DIR, name))
        if name in server_logs: del server_logs[name]
        if name in server_players: del server_players[name]
        return "✅ Deleted"
    except: return "❌ Failed"

@eel.expose
def start_server_py(ram):
    global current_view_server
    name = current_view_server
    if not name: return "❌ Select Server"
    if name in active_processes: return "⚠️ Running"
    jar = os.path.join(BASE_SERVERS_DIR, name, "server.jar")
    if not os.path.exists(jar): return "❌ No Jar"
    if name not in server_logs: server_logs[name] = []
    server_players[name] = {}
    if current_view_server == name: eel.update_player_list_js([])()
    t = threading.Thread(target=run_server, args=(name, jar, ram))
    t.daemon = True
    t.start()
    return "🚀 Starting..."

def run_server(name, jar, ram):
    d = os.path.dirname(jar)
    java = "java"
    try:
        with open(os.path.join(d, "nene_config.json"), 'r', encoding='utf-8') as f: java = json.load(f).get("java_path", "java")
    except: pass
    cmd = [java, f"-Xms{ram}G", f"-Xmx{ram}G", "-jar", os.path.basename(jar), "nogui"]
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW if os.name == 'nt' else 0
    try:
        p = subprocess.Popen(cmd, cwd=d, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', startupinfo=si)
        active_processes[name] = p
        if current_view_server == name: eel.update_status_js(True)()
        while True:
            line = p.stdout.readline()
            if not line and p.poll() is not None: break
            if line:
                clean = line.strip()
                append_log(name, clean)
                parse_player_event(name, clean)
        append_log(name, "[SYSTEM] Stopped")
        if name in active_processes: del active_processes[name]
        server_players[name] = {}
        if current_view_server == name: 
            eel.update_status_js(False)
            eel.update_player_list_js([])()
    except Exception as e:
        append_log(name, f"[ERROR] {e}")
        if name in active_processes: del active_processes[name]

def append_log(name, msg):
    if name not in server_logs: server_logs[name] = []
    server_logs[name].append(msg)
    if current_view_server == name: eel.add_log_js(msg)

def update_ui_player_list(server_name):
    if current_view_server == server_name:
        players = list(server_players.get(server_name, {}).keys())
        eel.update_player_list_js(players)()

def parse_player_event(server_name, line):
    if server_name not in server_players: server_players[server_name] = {}
    if "logged in with entity id" in line:
        try:
            parts = line.split(" logged in with entity id")
            raw = parts[0].strip().split(" ")[-1]
            name = raw.split("[")[0] if "[" in raw else raw
            name = re.sub(r'[^a-zA-Z0-9_]', '', name)
            if name:
                now = datetime.datetime.now().strftime("%H:%M:%S")
                server_players[server_name][name] = {"join_time": now, "uuid": "-"}
                update_ui_player_list(server_name)
        except: pass
    elif "lost connection" in line:
        try:
            parts = line.split(" lost connection")
            name = parts[0].strip().split(" ")[-1]
            name = re.sub(r'[^a-zA-Z0-9_]', '', name)
            if name in server_players[server_name]:
                del server_players[server_name][name]
                update_ui_player_list(server_name)
        except: pass

@eel.expose
def load_properties_py():
    if not current_view_server: return None
    props = {}
    d = os.path.join(BASE_SERVERS_DIR, current_view_server)
    try:
        with open(os.path.join(d, "server.properties"), 'r') as f:
            for l in f:
                if "=" in l and not l.startswith("#"):
                    k,v = l.strip().split("=", 1)
                    props[k] = v
    except: pass
    try:
        with open(os.path.join(d, "nene_config.json"), 'r', encoding='utf-8') as f: props.update(json.load(f))
    except: pass
    return props

@eel.expose
def save_properties_py(data):
    if not current_view_server: return "❌ No Server"
    d = os.path.join(BASE_SERVERS_DIR, current_view_server)
    current_conf = {}
    try:
        with open(os.path.join(d, "nene_config.json"), 'r', encoding='utf-8') as f: current_conf = json.load(f)
    except: pass
    
    special_keys = ["java_path", "auto_backup", "backup_interval"]
    for key in special_keys:
        if key in data:
            current_conf[key] = data[key]
            del data[key]

    try:
        with open(os.path.join(d, "nene_config.json"), 'w', encoding='utf-8') as f: json.dump(current_conf, f, indent=4)
        path = os.path.join(d, "server.properties")
        lines = []
        if os.path.exists(path):
            with open(path, 'r') as f: lines = f.readlines()
        else: lines = ["# Minecraft Properties\n"]
        final = []
        keys = []
        for l in lines:
            if "=" in l and not l.startswith("#"):
                k = l.split("=")[0].strip()
                if k in data:
                    final.append(f"{k}={str(data[k]).lower()}\n")
                    keys.append(k)
                else: final.append(l)
            else: final.append(l)
        for k,v in data.items():
            if k not in keys: final.append(f"{k}={str(v).lower()}\n")
        with open(path, 'w') as f: f.writelines(final)
        return "✅ Saved"
    except: return "❌ Failed"

@eel.expose
def check_java_status():
    try:
        subprocess.check_output([DEFAULT_JAVA, "-version"], stderr=subprocess.STDOUT)
        return {"status": "ok"}
    except: return {"status": "error"}

@eel.expose
def send_command_py(cmd):
    if current_view_server and current_view_server in active_processes:
        p = active_processes[current_view_server]
        if p.poll() is None:
            try: p.stdin.write(cmd+"\n"); p.stdin.flush(); append_log(current_view_server, f"> {cmd}")
            except: pass

@eel.expose
def trigger_backup_py(server_name):
    t = threading.Thread(target=backup_server, args=(server_name,))
    t.start()
    return "백업 시작됨"

def backup_server(server_name):
    try:
        server_dir = os.path.join(BASE_SERVERS_DIR, server_name)
        backup_dir = os.path.join(server_dir, "backups")
        if not os.path.exists(backup_dir): os.makedirs(backup_dir)
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_name = f"backup_{ts}.zip"
        zip_path = os.path.join(backup_dir, zip_name)
        if current_view_server == server_name: eel.add_log_js(f"[SYSTEM] 백업 중: {zip_name}")()
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for r, d, f in os.walk(server_dir):
                if "backups" in d: d.remove("backups")
                for file in f:
                    fp = os.path.join(r, file)
                    try: z.write(fp, os.path.relpath(fp, server_dir))
                    except: pass
        last_backup_times[server_name] = time.time()
        if current_view_server == server_name: eel.add_log_js("[SYSTEM] 백업 완료")()
    except Exception as e:
        if current_view_server == server_name: eel.add_log_js(f"[ERROR] 백업 실패: {e}")()

@eel.expose
def open_folder_py(server_name, mode):
    if not server_name: return "❌ No Server Selected"
    path = os.path.join(BASE_SERVERS_DIR, server_name)
    if mode == "backup":
        path = os.path.join(path, "backups")
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            return "❌ Create Failed"
    try:
        if os.name == 'nt': # Windows
            os.startfile(path)
        elif sys.platform == 'darwin': # macOS
            subprocess.Popen(['open', path])
        else: # Linux
            subprocess.Popen(['xdg-open', path])
        return "✅ Opened"
    except Exception as e:
        return f"❌ Error: {e}"

@eel.expose
def get_public_ip_py():
    try:
        return requests.get('https://api.ipify.org', timeout=3).text
    except:
        return "Unknown"

# ==========================================================
# [기능] 플러그인 관리 (Plugins)
# ==========================================================
@eel.expose
def get_plugin_list_py():
    if not current_view_server: return []
    
    plugins_dir = os.path.join(BASE_SERVERS_DIR, current_view_server, "plugins")
    if not os.path.exists(plugins_dir):
        try: os.makedirs(plugins_dir)
        except: return []
        
    plugin_list = []
    try:
        for file in os.listdir(plugins_dir):
            # .jar 파일 (켜짐)
            if file.endswith(".jar"):
                plugin_list.append({
                    "name": file,           # 표시 이름
                    "filename": file,       # 실제 파일명
                    "enabled": True
                })
            # .jar.disabled 파일 (꺼짐)
            elif file.endswith(".jar.disabled"):
                # 표시 이름은 .disabled 떼고 보여줌
                display_name = file.replace(".jar.disabled", ".jar")
                plugin_list.append({
                    "name": display_name,
                    "filename": file,
                    "enabled": False
                })
    except: pass
    
    # 이름 순 정렬
    return sorted(plugin_list, key=lambda x: x['name'])

@eel.expose
def toggle_plugin_py(filename, make_active):
    if not current_view_server: return "❌ No Server"
    plugins_dir = os.path.join(BASE_SERVERS_DIR, current_view_server, "plugins")
    old_path = os.path.join(plugins_dir, filename)
    
    if not os.path.exists(old_path): return "❌ File Not Found"
    
    try:
        if make_active:
            # 현재 .disabled 상태 -> .jar로 변경
            # 파일명이 ~~~.jar.disabled 라고 가정
            new_name = filename.replace(".jar.disabled", ".jar")
            new_path = os.path.join(plugins_dir, new_name)
            os.rename(old_path, new_path)
            return "✅ Enabled"
        else:
            # 현재 .jar 상태 -> .disabled로 변경
            new_name = filename + ".disabled"
            new_path = os.path.join(plugins_dir, new_name)
            os.rename(old_path, new_path)
            return "✅ Disabled"
    except Exception as e:
        return f"❌ Error: {e}"

@eel.expose
def delete_plugin_py(filename):
    if not current_view_server: return "❌ No Server"
    plugins_dir = os.path.join(BASE_SERVERS_DIR, current_view_server, "plugins")
    target_path = os.path.join(plugins_dir, filename)
    
    if not os.path.exists(target_path): return "❌ File Not Found"
    
    try:
        os.remove(target_path)
        return "✅ Deleted"
    except Exception as e:
        return f"❌ Error: {e}"

# ==========================================================
# [추가됨] 서버 상세 정보 (Server Info)
# ==========================================================
@eel.expose
def get_server_extended_info_py():
    if not current_view_server: return None
    
    server_path = os.path.join(BASE_SERVERS_DIR, current_view_server)
    config_path = os.path.join(server_path, "nene_config.json")
    
    # 기본값
    info = {
        "created_at": "Unknown",
        "source_url": "Unknown (Old Server)",
        "java_version": "Unknown",
        "disk_usage": "0 MB",
        "player_count": 0,
        "world_name": "world"
    }
    
    # 1. Config에서 정보 읽기 (생성일, 출처, 자바경로)
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                info["created_at"] = data.get("created_at", "Unknown")
                info["source_url"] = data.get("download_source", "Unknown (Old Server)")
                info["java_version"] = data.get("java_path", "java")
        except: pass

    # 생성일이 없으면(구버전) 폴더 생성 시간으로 추정
    if info["created_at"] == "Unknown":
        try:
            ctime = os.path.getctime(server_path)
            info["created_at"] = datetime.datetime.fromtimestamp(ctime).strftime("%Y-%m-%d %H:%M:%S")
        except: pass

    # 2. 디스크 사용량 계산
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(server_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        
        # MB 단위 변환
        mb_size = total_size / (1024 * 1024)
        if mb_size > 1024:
            info["disk_usage"] = f"{mb_size/1024:.2f} GB"
        else:
            info["disk_usage"] = f"{mb_size:.2f} MB"
    except: pass

    # 3. 플레이어 데이터 수 확인 (방문자 수 추정)
    # server.properties에서 level-name 확인
    try:
        prop_path = os.path.join(server_path, "server.properties")
        if os.path.exists(prop_path):
            with open(prop_path, 'r') as f:
                for line in f:
                    if line.startswith("level-name="):
                        info["world_name"] = line.split("=")[1].strip()
                        break
    except: pass

    try:
        playerdata_path = os.path.join(server_path, info["world_name"], "playerdata")
        if os.path.exists(playerdata_path):
            # .dat 파일 개수 세기
            count = len([name for name in os.listdir(playerdata_path) if name.endswith('.dat')])
            info["player_count"] = count
    except: pass

    return info

# ==========================================================
# [추가 기능] 자바 버전 관리자 (Java Version Manager)
# ==========================================================

# 전역 변수 업데이트를 위한 함수
def load_global_java_setting():
    global DEFAULT_JAVA
    try:
        if os.path.exists(LAUNCHER_CONFIG_FILE):
            with open(LAUNCHER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                conf = json.load(f)
                DEFAULT_JAVA = conf.get("global_java", "java")
    except: pass

@eel.expose
def scan_java_versions_py():
    """시스템에서 가능한 자바 경로들을 찾습니다."""
    java_list = []
    
    # 1. 현재 설정된 자바 (최상단)
    current_path = DEFAULT_JAVA
    current_ver = get_java_version_string(current_path)
    java_list.append({
        "path": current_path,
        "version": current_ver,
        "is_current": True
    })

    # 2. 시스템 PATH의 java
    if current_path != "java":
        sys_ver = get_java_version_string("java")
        if sys_ver != "Unknown":
            java_list.append({"path": "java", "version": sys_ver, "is_current": False})

    # 3. 일반적인 설치 경로 검색 (Windows 기준)
    search_paths = [
        r"C:\Program Files\Java",
        r"C:\Program Files (x86)\Java",
        r"C:\Program Files\Eclipse Adoptium",
        r"C:\Program Files\Zulu",
        r"C:\Program Files\Microsoft",
        r"C:\Program Files\BellSoft"
    ]

    for root_dir in search_paths:
        if os.path.exists(root_dir):
            for item in os.listdir(root_dir):
                full_path = os.path.join(root_dir, item, "bin", "java.exe")
                if os.path.exists(full_path) and full_path != current_path:
                    ver = get_java_version_string(full_path)
                    if ver != "Unknown":
                        java_list.append({
                            "path": full_path,
                            "version": ver,
                            "is_current": False
                        })
    
    # 중복 제거
    unique_list = []
    seen_paths = set()
    for j in java_list:
        if j['path'] not in seen_paths:
            unique_list.append(j)
            seen_paths.add(j['path'])
            
    return unique_list

def get_java_version_string(path):
    try:
        # java -version은 stderr로 출력됩니다.
        cmd = [path, "-version"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stderr
        
        # 버전 문자열 파싱 (ex: "1.8.0_202" or "17.0.1")
        for line in output.split('\n'):
            if "version" in line:
                return line.split('"')[1]
        return "Detected"
    except:
        return "Unknown"

@eel.expose
def set_global_java_py(new_path):
    # 서버 실행 중인지 확인
    if len(active_processes) > 0:
        return "⚠️ Running"

    try:
        # 설정 파일 로드 및 업데이트
        config = {}
        if os.path.exists(LAUNCHER_CONFIG_FILE):
            with open(LAUNCHER_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config["global_java"] = new_path
        
        with open(LAUNCHER_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            
        global DEFAULT_JAVA
        DEFAULT_JAVA = new_path
        return "✅ Saved"
    except Exception as e:
        return f"❌ Error: {e}"

@eel.expose
def check_any_server_running_py():
    return len(active_processes) > 0


def close_callback(route, websockets):
    pass

def create_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (60, 166, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
    return image

def quit_app(icon, item):
    icon.stop()
    for p in active_processes.values():
        try: p.terminate()
        except: pass
    os._exit(0)

def open_browser(icon, item):
    webbrowser.open('http://localhost:8000/index.html')

def setup_tray():
    image = create_image()
    if os.path.exists("icon.ico"):
        try: image = Image.open("icon.ico")
        except: pass
        
    menu = (
        pystray.MenuItem('Open Dashboard', open_browser, default=True),
        pystray.MenuItem('Quit', quit_app)
    )
    icon = pystray.Icon("nene_helper", image, "NENE HELPER", menu)
    icon.run()

def system_monitor_thread():
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            eel.update_cpu_usage_js(cpu)
            cur = time.time()
            for name in list(active_processes.keys()):
                if active_processes[name].poll() is None:
                    try:
                        cp = os.path.join(BASE_SERVERS_DIR, name, "nene_config.json")
                        if os.path.exists(cp):
                            with open(cp, 'r', encoding='utf-8') as f:
                                conf = json.load(f)
                                if conf.get("auto_backup", False):
                                    iv = int(conf.get("backup_interval", 60)) * 60
                                    lst = last_backup_times.get(name, 0)
                                    if lst == 0: last_backup_times[name] = cur
                                    elif (cur - lst) >= iv: backup_server(name)
                    except: pass
        except: pass

if __name__ == "__main__":
    t = threading.Thread(target=system_monitor_thread)
    t.daemon = True
    t.start()
    
    t_tray = threading.Thread(target=setup_tray, daemon=True)
    t_tray.start()
    
    webbrowser.open('http://localhost:8000/index.html')
    
    try: 
        eel.start('index.html', mode=False, port=8000, host='localhost', block=True, close_callback=close_callback)
    except Exception as e:
        pass