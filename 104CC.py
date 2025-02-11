'''104職缺爬蟲'''
import requests
import json
import time
import csv

def get_jobs_data(keyword, pages=9):
    session = requests.Session()
    
    # 首先訪問搜索頁面獲取 Cookie
    session.get(
        "https://www.104.com.tw/jobs/search/",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.104.com.tw/jobs/search/",
        "Origin": "https://www.104.com.tw"
    }
    
    base_params = {
        "keyword": keyword,
        "mode": "s",
        "jobsource": "2018indexpoc",
        "ro": "0",
        "kwop": "7",
        "order": "12",
        "asc": "0",
        "page": "1",
        "format": "json"
    }
    
    # 準備CSV文件
    with open('104_jobs.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            '公司名稱',
            '職缺名稱',
            '工作地點',
            '薪資',
            '更新日期',
            '工作性質',
            '管理責任',
            '出差外派',
            '上班時段',
            '休假制度',
            '可上班日',
            '需求人數',
            '接受身份',
            '工作經歷',
            '學歷要求',
            '科系要求',
            '語文條件'
        ])
        
        for page in range(1, pages + 1):
            print(f"\n正在獲取第 {page} 頁...")
            
            params = base_params.copy()
            params["page"] = str(page)
            
            response = session.get("https://www.104.com.tw/jobs/search/list", headers=headers, params=params)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    jobs = data.get("data", {}).get("list", [])
                    
                    for job in jobs:
                        row_data = [
                            job.get('custNameRaw', ''),  # 公司名稱
                            job.get('jobNameRaw', ''),   # 職缺名稱
                            job.get('jobArea', ''),      # 工作地點
                            job.get('salaryRaw', ''),    # 薪資
                            job.get('updateDate', ''),   # 更新日期
                            job.get('jobType', ''),      # 工作性質
                            job.get('manageResp', ''),   # 管理責任
                            job.get('remoteWork', ''),   # 出差外派
                            job.get('workPeriod', ''),   # 上班時段
                            job.get('holidayPolicy', ''), # 休假制度
                            job.get('startWork', ''),    # 可上班日
                            job.get('needEmp', ''),      # 需求人數
                            job.get('role', ''),         # 接受身份
                            job.get('workExp', ''),      # 工作經歷
                            job.get('edu', ''),          # 學歷要求
                            job.get('major', ''),        # 科系要求
                            job.get('language', '')      # 語文條件
                        ]
                        writer.writerow(row_data)
                        print(f"已寫入資料: {row_data[0]} - {row_data[1]}")
                    
                    print(f"第 {page} 頁成功獲取 {len(jobs)} 個職缺")
                    time.sleep(2)
                    
                except json.JSONDecodeError as e:
                    print(f"第 {page} 頁解析失敗: {str(e)}")
                    continue
            else:
                print(f"第 {page} 頁請求失敗: {response.status_code}")

    print("\n爬蟲完成！")
    print("數據已保存到 104_jobs.csv")

if __name__ == "__main__":
    try:
        keyword = input("請輸入要搜尋的職缺關鍵字：")
        get_jobs_data(keyword)
    except Exception as e:
        print(f"發生錯誤：{str(e)}")