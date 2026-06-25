import os
import requests
from bs4 import BeautifulSoup

# URL trang tổng hợp thông tin TCG uy tín tại Nhật
SOURCES = [
    {
        "name": "Pokemon Center",
        "url": "https://www.pokemoncenter-online.com"
    },

    {
        "name": "Joshin",
        "url": "https://joshinweb.jp"
    },

    {
        "name": "Bic Camera",
        "url": "https://www.biccamera.com"
    },

    {
        "name": "Yodobashi",
        "url": "https://www.yodobashi.com"
    }
]
# Link Webhook Discord của bạn
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/ID/TOKEN"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_latest_posts(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )

        if response.status_code != 200:
            print(
                f"Không thể kết nối. Mã lỗi: {response.status_code}"
            )
            return []

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        posts = []

        links = soup.find_all("a")

        for a_tag in links:
            title = a_tag.text.strip()
            link = a_tag.get("href", "")

            if len(title) > 10:
                posts.append({
                    "title": title,
                    "link": link
                })

        return posts

    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")
        return []
if response.status_code != 200:
    print(f"Không thể kết nối trang web Nhật. Mã lỗi: {response.status_code}")
    return []
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        
        # Cấu trúc quét mở rộng: Lấy tất cả các liên kết bài viết trên trang
        links = soup.find_all('a')
        for a_tag in links:
            title = a_tag.text.strip()
            link = a_tag.get('href', '')
            
            # Chỉ lấy các link bài viết hợp lệ từ trang nguồn, bỏ qua link rác
            if len(title) > 10:
                posts.append({"title": title, "link": link})
                
        return posts
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")
        return []

def send_to_discord(title, link):
    content = f"🚨 **CÓ SỰ KIỆN CHYUSEN MỚI!** 🚨\n📌 **Tên:** {title}\n🔗 **Link đăng ký:** {link}"
    payload = {"content": content}
    try:
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print(f"Trạng thái gửi Discord: {res.status_code}")
    except Exception as e:
        print(f"Lỗi gửi Discord: {e}")

def main():

    for source in SOURCES:

        print(f"\n===== {source['name']} =====")

        posts = get_latest_posts(source["url"])

        print(f"Tìm thấy {len(posts)} bài")
    keywords = [
 "抽選",
 "抽選販売",
 "応募開始",
 "応募受付",
 "受付開始",
 "販売開始",
 "当選",
 "ポケモン",
 "ポケカ",
 "ワンピース",
 "ONE PIECE"
]
    
    # Đọc danh sách các bài viết cũ đã thông báo để tránh trùng lặp
    history_file = "history.txt"
    sent_links = set()
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            sent_links = set(f.read().splitlines())

    new_links = []
    for post in posts:
        title_upper = post["title"].upper()
        # Nếu tiêu đề chứa từ khóa và chưa từng gửi thông báo trước đây
        if any(kw.upper() in title_upper for kw in keywords) and post["link"] not in sent_links:
            print(f"Phát hiện chyusen mới: {post['title']}")
           send_to_discord(post["title"], post["link"])

 content = f"..."

    payload = {"content": content}

    res = requests.post(
        DISCORD_WEBHOOK_URL,
        json=payload
    )

    print("Discord status:", res.status_code)
print(res.text)
            new_links.append(post["link"])
            
    # Lưu các link mới vào lịch sử để lần sau không bắn trùng
    if new_links:
        with open(history_file, "a", encoding="utf-8") as f:
            for link in new_links:
                f.write(f"{link}\n")

if __name__ == "__main__":
    # Chỉ chạy quét dữ liệu thực tế, đã gỡ bỏ hoàn toàn tin nhắn thử nghiệm rác
    main()
