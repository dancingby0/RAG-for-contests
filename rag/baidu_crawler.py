import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import random
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor


def crawl_single_page(page, keyword, encoded_keyword, output_file, headers):
    while True:  # 持续尝试直到成功
        url = f"https://zhidao.baidu.com/search?word={encoded_keyword}&pn={(page-1)*10}"
        try:
            print(f"正在爬取第{page}页...")
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "html.parser")

            # 尝试不同的选择器
            questions = (
                soup.select("dl.dl")
                or soup.select(".list-inner")
                or soup.select(".wgt-best")
                or soup.select(".question-title")
                or soup.select(".list-item")
            )

            success = False
            if questions:
                with open(output_file, "a", encoding="utf-8") as f:
                    for question in questions:
                        try:
                            title = (
                                question.select_one("a.ti")
                                or question.select_one(".question-title a")
                                or question.select_one("dt a")
                            )

                            answer = (
                                question.select_one(".dec")
                                or question.select_one(".answer-text")
                                or question.select_one("dd.answer")
                            )

                            if title and answer:
                                # 获取完整的文本内容，保留原始格式
                                question_text = " ".join(title.stripped_strings)
                                answer_text = " ".join(answer.stripped_strings)

                                if question_text and answer_text:
                                    # 写入完整的问答内容
                                    f.write(f"问：{question_text}\n")
                                    f.write(f"答：{answer_text}\n\n")
                                    f.flush()
                                    print(f"成功爬取第{page}页的一条问答")
                                    success = True

                        except Exception as e:
                            print(f"处理第{page}页单个问答时出错: {e}")
                            continue

            if success:
                break  # 如果成功爬取到内容就退出循环
            else:
                print(f"第{page}页未找到内容，等待后重试...")
                time.sleep(random.uniform(3, 6))

        except requests.exceptions.RequestException as e:
            print(f"爬取第{page}页时出错: {e}")
            time.sleep(5)
            continue


def crawl_baidu_zhidao(keyword, output_file):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Cookie": "BAIDUID="
        + "".join(random.choice("0123456789ABCDEF") for _ in range(32)),
    }

    encoded_keyword = urllib.parse.quote(keyword)

    with open(output_file, "a", encoding="utf-8") as f:
        f.write(
            f"\n\n# 关键词：{keyword} - 爬取时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

    # 使用线程池进行并发爬取
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for page in range(1, 11):
            futures.append(
                executor.submit(
                    crawl_single_page,
                    page,
                    keyword,
                    encoded_keyword,
                    output_file,
                    headers.copy(),
                )
            )
        # 等待所有任务完成
        for future in futures:
            future.result()


if __name__ == "__main__":
    keyword = input("请输入要搜索的关键词：")
    output_file = "d:/pathonpro/pythonProject6/RAG本地运行/baidu_knowledge.txt"
    print(f"开始爬取关于 '{keyword}' 的问答内容...")
    crawl_baidu_zhidao(keyword, output_file)
    print(f"爬取完成！结果已保存到：{output_file}")
