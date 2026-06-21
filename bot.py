import os
import requests
from bs4 import BeautifulSoup

# URL trang tổng hợp chyusen uy tín tại Nhật
TARGET_URL = "https://pokeka-center.com" 
# Link Webhook Discord bạn lấy từ app Discord (Thay đoạn dưới này bằng link của bạn)
DISCORD_WEBHOOK_URL = "https://discord.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_latest_posts():
    try:
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = []
        
        # Tìm tất cả các thẻ tiêu đề chứa link bài viết trên trang
        for article in soup.find_all('h2', class_='entry-title'):
            a_tag = article.find('a')
            if a_tag:
                title = a_tag.text.strip()
                link = a_tag['href']
                posts.append({"title": title, "link": link})
        return posts
    except Exception as e:
        print(f"Lỗi khi cào dữ liệu: {e}")
        return []

def send_to_discord(title, link):
    content = f"🚨 **CÓ SỰ KIỆN CHYUSEN MỚI!** 🚨\n📌 **Tên:** {title}\n🔗 **Link đăng ký:** {link}"
    payload = {"content": content}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

def main():
    posts = get_latest_posts()
    
    # Từ khóa lọc sự kiện rút thăm One Piece và Pokemon bằng tiếng Nhật
    keywords = ["抽選", "ONE PIECE", "ワンピース", "ポケモン", "ポケカ"]
    
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
            new_links.append(post["link"])
            
    # Lưu các link mới vào lịch sử để lần sau không bắn trùng
    if new_links:
        with open(history_file, "a", encoding="utf-8") as f:
            for link in new_links:
                f.write(f"{link}\n")

if __name__ == "__main__":
    main()
