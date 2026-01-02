import requests, sys, time, json, threading, random, re, os
from urllib.parse import urlparse, parse_qs
from pystyle import *
import concurrent.futures

ducvannguyen = "Trần Minh Triết x Duc Van Nguyen"
project = "Buff xu hosting (https://bot-hosting.net/)"
fb = "https://www.facebook.com/ducvannguyen.html & https://www.facebook.com/ducvannguyen.it"
zalo = "0359261551"
dis = "or username: _thick1minh"

rawlinks = [
    "https://raw.githubusercontent.com/giakietdev/art/master/ak.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/boss.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/bucu.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/cu.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/daulau.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/daulau2.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/du1.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/fuck.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/galaxy.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/gojo.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/hacker.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/hacker2.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/hacker3.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/hacker4.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/hellokitty.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/iloveyou.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/iloveyou2.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/kawaii.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/lacdit.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/like.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/meo.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/nooooooooooo.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/pokemon.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/rose.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/sad.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/sao.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/sao2.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/sut.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/tim.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/troll.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/tym.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/tym2.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/tym3.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/tymvo.hoanggiakiet",
    "https://raw.githubusercontent.com/giakietdev/art/master/uno.hoanggiakiet"
]
banner = f"""
                                                       
    ▄▄▄          ▄▄  ▄▄   ▄   ▄▄▄▄                     
   ██▀▀█▄       ██  ██    ▀██████▀                     
   ██ ▄█▀      ▄██▄▄██▄     ██           ▀▀ ▄          
   ██▀▀█▄ ██ ██ ██  ██      ██     ▄███▄ ██ ████▄ ▄██▀█
 ▄ ██  ▄█ ██ ██ ██  ██      ██     ██ ██ ██ ██ ██ ▀███▄
 ▀██████▀▄▀██▀█▄██ ▄██      ▀█████▄▀███▀▄██▄██ ▀██▄▄██▀
                ██  ██                                 
               ▀▀  ▀▀                                  

"""

info = f"""
                                         Author: {ducvannguyen}
                                       PJ: {project}
                    FB: {fb}
                         Dis: {dis}

"""
linkaff = """
                              Lấy link affiliate ở: https://bot-hosting.net/panel/affiliate
                              
                            """
def loadapi(threads):
    apikeys = []
    try:
        with open("apiKey.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                key = line.strip()
                if key:
                    apikeys.append(key)
    except FileNotFoundError:
        print(Colorate.Vertical(Colors.red_to_white, "[ERROR] apiKey.txt ko tồn tại"))
        sys.exit()
    if len(apikeys) < threads:
        print(Colorate.Vertical(Colors.red_to_white, f"[ERROR] Ko đủ api key dành cho {threads} luồng, hiện chỉ có {len(apikeys)}"))
        sys.exit()
    return apikeys[:threads]

def getAffID(link):
    try:
        parsed = urlparse(link)
        query_params = parse_qs(parsed.query)
        if 'aff' in query_params:
            return query_params['aff'][0]
        return None
    except:
        return None

def getNewPrx(key, province_id=-1):
    url = f"https://wwproxy.com/api/client/proxy/available?key={key}&provinceId={province_id}"
    while True:
        try:
            r = requests.get(url, timeout=15)
            data = r.json()
            if data.get("status") == "OK" and data.get("data"):
                p = data["data"]
                ip = p["ipAddress"]
                port = p["port"]
                proxy_full = p["proxy"]
                proxy_url = f"http://{proxy_full}" if "@" in proxy_full else f"http://{ip}:{port}"
                print(Colorate.Vertical(Colors.green_to_cyan, f"[Proxy Success] Lấy proxy thành công: {ip}:{port}"))
                return {"http": proxy_url, "https": proxy_url}, ip, port
            if data.get("status") == "BAD_REQUEST":
                message = data.get("message", "")
                if "Khóa đã hết hạn" in message or "hết hạn" in message.lower():
                    os._exit(1) 
                if "Vui lòng chờ thêm" in message:
                    try:
                        match = re.search(r'chờ thêm (\d+)s', message)
                        if match:
                            seconds = int(match.group(1))
                            wait_time = seconds + 1
                            time.sleep(wait_time)
                            continue
                    except:
                        pass
                    time.sleep(35)
                    continue
            error_msg = data.get("message", "Unknown error")
            time.sleep(15)
        except Exception as e:
            time.sleep(15)

def luutoken(done_tokens):
    os.makedirs("output", exist_ok=True)
    with open("output/tokenBuffDone.txt", "a", encoding="utf-8") as f:
        for tk in done_tokens:
            f.write(tk + "\n")

def xoatokendone(done_tokens):
    try:
        with open("tokens.txt", "r", encoding="utf-8") as f:
            all_tokens = [line.strip() for line in f if line.strip()]
        remaining_tokens = [tk for tk in all_tokens if tk not in done_tokens]
        with open("tokens.txt", "w", encoding="utf-8") as f:
            for tk in remaining_tokens:
                f.write(tk + "\n")
    except:
        pass

def QuangThangDepTrai():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        threads = config.get("threads", 1)
        random_location = config.get("randomLocation", True)
        location_mode = config.get("Location", False)
        stt_list = config.get("STT", [])
        if isinstance(stt_list, str):
            stt_list = [int(x.strip()) for x in stt_list.split(",") if x.strip().isdigit()]
        elif isinstance(stt_list, list):
            stt_list = [int(x) for x in stt_list if str(x).isdigit()]
        if not stt_list:
            province_ids = [-1]
        else:
            if random_location:
                province_ids = [-1]
            else:
                if location_mode:
                    province_ids = stt_list
                else:
                    fixed_id = stt_list[0]
                    province_ids = [fixed_id]
    except Exception as e:
        threads = 1
        province_ids = [-1]

    print(Colorate.Vertical(Colors.cyan_to_blue, "Nhập Link Affiliate: "), end="")
    afflink = input().strip()
    affid = getAffID(afflink)
    if not affid:
        print(Colorate.Vertical(Colors.red_to_white, f"[Duc Van Nguyen | System | Không tìm thấy tham số 'aff=' trong link. Vui lòng kiểm tra lại!]"))
        return
    print(Colorate.Vertical(Colors.cyan_to_blue, f"[Duc Van Nguyen | System | Affiliate ID Cần Buff: {affid}]"))

    filetoken = "tokens.txt"
    apikeys = loadapi(threads)
    if len(apikeys) < threads:
        print(Colorate.Vertical(Colors.red_to_white, f"[Duc Van Nguyen | System | Chỉ nhập {len(apikeys)} key nhưng cần {threads} key!]"))
        return

    try:
        with open(filetoken, "r", encoding="utf-8") as f:
            tokens = [line.strip() for line in f if line.strip()]
        if not tokens:
            print(Colorate.Vertical(Colors.red_to_white, f"[Duc Van Nguyen | System | File token trống]"))
            return
    except Exception as e:
        print(Colorate.Vertical(Colors.red_to_white, f"[Duc Van Nguyen | System | Lỗi đọc file token: {e}]"))
        return

    print(Colorate.Vertical(Colors.cyan_to_blue, f"[Duc Van Nguyen | System | Đã tải {len(tokens)} token. Bắt đầu buff với {threads} luồng...]"))
    time.sleep(2)

    threadtoken = [tokens[i::threads] for i in range(threads)]
    threadslist = []
    alltokendone = []
    lock = threading.Lock()

    for i in range(threads):
        thread_province_ids = province_ids.copy()
        t = threading.Thread(target=anhkiet, args=(affid, afflink, threadtoken[i], apikeys[i], i+1, thread_province_ids, lock, alltokendone))
        threadslist.append(t)
        t.start()
    
    for t in threadslist:
        t.join()

    if alltokendone:
        luutoken(alltokendone)
        xoatokendone(alltokendone)
    
    print(Colorate.Vertical(Colors.yellow_to_green, f"\nHoàn thành tất cả luồng! Đã buff thành công {len(alltokendone)} token và di chuyển vào output/tokenBuffDone.txt"))

def anhkiet(affid, afflink, tokens, apikey, thread_id, province_ids, lock, alltokendone):
    success_count = 0
    failed_count = 0 

    for idx, tk in enumerate(tokens, 1):
        token_skipped = False

        while not token_skipped:
            print(Colorate.Vertical(Colors.cyan_to_blue, f"[Thread {thread_id} | Duc Van Nguyen | System | [{idx}/{len(tokens)}] Đang xử lý token: {tk[:15]}...]"))
            selected_province = random.choice(province_ids)
            if selected_province == -1:
                print(Colorate.Vertical(Colors.cyan_to_blue, f"[Thread {thread_id} | Proxy | {idx}] Lấy proxy random toàn quốc"))
            else:
                print(Colorate.Vertical(Colors.cyan_to_blue, f"[Thread {thread_id} | Proxy | {idx}] Lấy proxy tỉnh ID: {selected_province}"))
            current_proxy, current_ip, current_port = getNewPrx(apikey, selected_province)

            try:
                geo_response = requests.get(f"http://ip-api.com/json/{current_ip}", timeout=5)
                geo = geo_response.json()
                if geo.get('status') == 'success':
                    location = f"{geo.get('city', 'Unknown')}, {geo.get('regionName', 'Unknown')}, {geo.get('country', 'Unknown')}"
                    isp = geo.get('isp', 'Unknown')
                else:
                    location = "Unknown"
                    isp = "Unknown"
                print(Colorate.Vertical(Colors.cyan_to_blue, f"[Thread {thread_id} | Proxy | {idx}] IP: {current_ip}:{current_port} | {location} | {isp}]"))
            except:
                print(Colorate.Vertical(Colors.red_to_white, f"[Thread {thread_id} | Proxy Info Error] Không lấy được info vị trí"))

            try:
                s = requests.Session()
                s.proxies.update(current_proxy)
                ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
                xsp = "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InZpLVZOIiwiaGFzX2NsaWVudF9tb2RzIjpmYWxzZSwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEwOyBLKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTM3LjAuMC4wIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMzcuMC4wLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiaHR0cHM6Ly9ib3QtaG9zdGluZy5uZXQvIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiYm90LWhvc3RpbmcubmV0IiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6NDYzMzExLCJjbGlieW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiY2xpZW50X2xhdW5jaF9pZCI6ImVjODY4MjI4LWJhMWMtNDU0Yi05N2NjLTY0ZDVjYzUwMDljZSIsImxhdW5jaF9zaWduYXR1cmUiOiJlOTQzODkyNS1iNzgxLTQ1NTItOGY0Ni0wYjdkZTBjMDU0MCIsImNsaWVudF9oZWFydGJlYXRfc2Vzc2lvbl9pZCI6IjhlMjFjZTQ4LWU1MDItNDgxNS05MjY1LTU2ODkwOWU4OGMwNyIsImNsaWVudF9hcHBfc3RhdGUiOiJmb2N1c2VkIn0="
                for attempt in range(3):
                    try:
                        s.get(afflink, timeout=20)
                        s.get("https://bot-hosting.net/panel", headers={"User-Agent": ua, "Referer": afflink}, timeout=20)
                        s.get("https://bot-hosting.net/login", headers={"User-Agent": ua, "Referer": "https://bot-hosting.net/panel"}, timeout=20)
                        break
                    except:
                        if attempt < 2:
                            print(Colorate.Vertical(Colors.yellow_to_red, f"[Thread {thread_id} | Retry {attempt+1}/3] Lỗi kết nối trang chính → lấy proxy mới..."))
                            current_proxy, current_ip, current_port = getNewPrx(apikey, selected_province)
                            s.proxies.update(current_proxy)
                            time.sleep(3)
                        else:
                            raise

                oauth_ref = "https://discord.com/oauth2/authorize?client_id=884382422530158623&redirect_uri=https%3A%2F%2Fbot-hosting.net%2Fpanel%2F&response_type=code&scope=identify+email+guilds.join"
                hdr = {
                    "Authorization": tk,
                    "User-Agent": ua,
                    "Referer": oauth_ref,
                    "X-Super-Properties": xsp,
                    "X-Discord-Locale": "vi",
                    "X-Discord-Timezone": "Asia/Bangkok",
                    "X-Debug-Options": "bugReporterEnabled"
                }
                requests.get(
                    "https://discord.com/api/v9/oauth2/authorize?client_id=884382422530158623&response_type=code&redirect_uri=https%3A%2F%2Fbot-hosting.net%2Fpanel%2F&scope=identify%20email%20guilds.join&integration_type=0",
                    headers=hdr, proxies=current_proxy, timeout=20
                )
                hdr.update({
                    "Content-Type": "application/json", 
                    "Origin": "https://discord.com"
                    })
                body = {
                    "permissions": "0",
                    "authorize": True,
                    "integration_type": 0,
                    "location_context": {"guild_id": "10000", "channel_id": "10000", "channel_type": 10000},
                    "dm_settings": {"allow_mobile_push": False}
                }
                r = requests.post(
                    "https://discord.com/api/v9/oauth2/authorize?client_id=884382422530158623&response_type=code&redirect_uri=https%3A%2F%2Fbot-hosting.net%2Fpanel%2F&scope=identify%20email%20guilds.join",
                    headers=hdr, json=body, proxies=current_proxy, timeout=20
                )
                resp_json = r.json()
                if "location" not in resp_json:
                    print(Colorate.Vertical(Colors.red_to_white, f"[Thread {thread_id} | FAILED | {idx}] Token die hoặc chưa verify → BỎ QUA token này!"))
                    failed_count += 1
                    token_skipped = True 
                    break

                code = resp_json["location"].split("code=")[1]
                s.post(
                    "https://bot-hosting.net/api/login",
                    headers={
                        "User-Agent": ua,
                        "Content-Type": "application/json",
                        "Referer": f"https://bot-hosting.net/panel/?code={code}"
                    },
                    json={"code": code, "affiliate": affid},
                    timeout=20
                )
                print(Colorate.Vertical(Colors.green_to_cyan, f"[Thread {thread_id} | Success | {idx}] Buff thành công! Token: {tk[:15]}... | IP: {current_ip}:{current_port}]"))
                success_count += 1

                with lock:
                    alltokendone.append(tk)

                token_skipped = True 
                break

            except Exception as e:
                print(Colorate.Vertical(Colors.red_to_white, f"[Thread {thread_id} | Error | {idx}] {str(e)[:120]} → thử lại với proxy mới..."))
                time.sleep(3)
        time.sleep(2) 
    print(Colorate.Vertical(Colors.yellow_to_green, f"[Thread {thread_id}] Hoàn thành: {success_count}/{len(tokens)} thành công, {failed_count} token die bị bỏ qua"))
def bannerraw():
    def download_art(url):
        try:
            response = requests.get(url, timeout=8)
            if response.status_code == 200 and response.text.strip():
                return response.text
        except:
            pass
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=35) as executor:
        arts = list(executor.map(download_art, rawlinks))
    arts = [art for art in arts if art]
    colors_list = [
        Colors.cyan_to_blue,
        Colors.green_to_cyan,
        Colors.blue_to_purple,
        Colors.red_to_yellow,
        Colors.yellow_to_green,
        Colors.purple_to_blue
    ]

    for i, art in enumerate(arts):
        os.system('cls' if os.name == 'nt' else 'clear')
        title = rawlinks[i].split('/')[-1].replace(".ducvannguyen", "").upper()
        print(Colorate.Vertical(random.choice(colors_list), Center.Center(art)))
        time.sleep(0.09) 
    os.system('cls' if os.name == 'nt' else 'clear')
if __name__ == "__main__":
    bannerraw()
    print(Colorate.Vertical(Colors.cyan_to_blue, Center.Center(banner)))
    print(Colorate.Vertical(Colors.cyan_to_blue, info))
    print(Colorate.Vertical(Colors.cyan_to_blue, linkaff))
    QuangThangDepTrai()