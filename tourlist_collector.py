import requests
import psycopg2
import time
import urllib3
urllib3.disable_warnings()



# 🔑 TourAPI 디코딩된 인증키
SERVICE_KEY = "DUZ7d6Gh1UXHBGbd5/MYj0DXqppwedSd3GCDWclNv5UyfCdpfoUicuVgdD+N+ESsb+q1TiW14UXyJ9v2hGy3FQ=="

# 🛢️ PostgreSQL 접속 정보
DB_CONFIG = {
    "host": "dpg-d275la95pdvs73cd2e10-a.oregon-postgres.render.com",
    "port": 5432,
    "dbname": "crowdanalysis",
    "user": "crowdanalysis_user",
    "password": "EpeuXBKHEwoEJl4366SGIEEZo6G318Tk"
}

def create_table_if_not_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tourist_spot (
            content_id TEXT PRIMARY KEY,
            title TEXT,
            address TEXT,
            mapx DOUBLE PRECISION,
            mapy DOUBLE PRECISION,
            area_code TEXT,
            sigungu_code TEXT
        )
    """)

def insert_tourist_data(cursor, item):
    cursor.execute("""
        INSERT INTO tourist_spot (content_id, title, address, mapx, mapy, area_code, sigungu_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (content_id) DO NOTHING
    """, (
        str(item.get("contentid")),
        item.get("title", ""),
        item.get("addr1", ""),
        float(item.get("mapx", 0)),
        float(item.get("mapy", 0)),
        str(item.get("areacode", "")),
        str(item.get("sigungucode", ""))
    ))

def collect_tourist_data_from_api():
    base_url = "http://apis.data.go.kr/B551011/KorService2/areaBasedList2"
    page_no = 1
    num_of_rows = 100
    total_saved = 0

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    create_table_if_not_exists(cursor)

    while True:
        params = {
            "serviceKey": "DUZ7d6Gh1UXHBGbd5/MYj0DXqppwedSd3GCDWclNv5UyfCdpfoUicuVgdD+N+ESsb+q1TiW14UXyJ9v2hGy3FQ==",
            "numOfRows": num_of_rows,
            "pageNo": page_no,
            "MobileOS": "ETC",
            "MobileApp": "FastAPIApp",
            "_type": "json",
            "arrange": "C",
            "contentTypeId": "12"
        }
        print(requests)
        response = requests.get(base_url, params=params)  # ✅ SSL 무시
        print(response.text)

        data = response.json()

        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
        if not items:
            break

        for item in items:
            insert_tourist_data(cursor, item)
            total_saved += 1

        conn.commit()
        page_no += 1
        time.sleep(0.3)  # API Rate Limit 대응

    cursor.close()
    conn.close()

    return total_saved


def get_tourist_spots():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT content_id, title, address, mapx, mapy
        FROM tourist_spot
    """)
    rows = cursor.fetchall()

    # 컬럼 이름 가져오기
    columns = [desc[0] for desc in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()
    return result
