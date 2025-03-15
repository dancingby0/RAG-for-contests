import os


def add_knowledge_to_file(knowledge_text):
    """向知识库文件添加新的知识"""
    file_path = "d:/pathonpro/pythonProject6/RAG本地运行/example.txt"

    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 添加新知识到文件
        with open(file_path, "a", encoding="utf-8") as f:
            # 确保新知识从新行开始
            f.write("\n" + knowledge_text.strip() + "\n")
        print("成功添加新知识到文件")
        return True
    except Exception as e:
        print(f"添加知识时出错: {e}")
        return False


def view_knowledge():
    """查看当前知识库内容"""
    file_path = "d:/pathonpro/pythonProject6/RAG本地运行/example.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("当前知识库内容：")
        print(content)
    except Exception as e:
        print(f"读取知识库时出错: {e}")


if __name__ == "__main__":
    while True:
        print("\n=== 知识库管理系统 ===")
        print("1. 添加新知识")
        print("2. 查看知识库")
        print("3. 退出")

        choice = input("请选择操作 (1-3): ")

        if choice == "1":
            knowledge = input("请输入要添加的知识：\n")
            add_knowledge_to_file(knowledge)
        elif choice == "2":
            view_knowledge()
        elif choice == "3":
            print("退出系统")
            break
        else:
            print("无效的选择，请重试")
