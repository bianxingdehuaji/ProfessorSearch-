import pyalex
pyalex.config.api_key = "API_KEY_HERE"

#调用开源项目PyAlex，并配置 API 密钥.（若未配置正确的 API 密钥，程序将无法运行.） Call the open-source project PyAlex and configure the API key.(If the correct API key is not configured, the program will not run.)

#关于 API 密钥的详细信息，参见 README 文件 3.3. For details regarding API keys, please refer to the 3.3 chapter in README file.

from pyalex import Authors
name = input("请输入作者姓名（建议使用英文）：").strip()
authors = Authors().search(name).get(per_page=10)

#询问用户，调用PyAlex搜索.此处可以指定单次出现的搜索条目数量.

if not authors:
    print("没有找到匹配的作者.请检查姓名拼写后重试。")

#当没有搜索结果时，返回“未匹配”.

#出现搜索结果后，获取归属机构，论文数量，应用数量等信息.将同名教授列为表格，等待下一步筛选.

else:
    print("\n找到的作者：")
    for number, author in enumerate(authors, start=1):
        institutions = author.get("last_known_institutions") or []
        if institutions:
            institution_names = "、".join(
                institution.get("display_name", "未知机构")
                for institution in institutions[:2]
            )
        else:
            institution_names = "未提供"

        print(
            number, ".",
            author.get("display_name", "未知姓名"),
            "｜论文数量：", author.get("works_count", "未知"),
            "｜总引用次数：", author.get("cited_by_count", "未知")
        )
        print("   所属组织：", institution_names)
#用户选择指定的教授，展示详细信息

while True:
        choice = input("\n请输入想查看的作者编号：").strip()

#返回教授的基础信息，H指数和i10指数信息

        try:
            selected_author = authors[int(choice) - 1]

            print("\n===== 作者详细信息 =====")
            print("姓名：", selected_author.get("display_name", "未知"))
            print("OpenAlex 编号：", selected_author.get("id", "未知"))
            print("ORCID：", selected_author.get("orcid", "未提供"))
            print("论文总数：", selected_author.get("works_count", "未知"))
            print("总引用次数：", selected_author.get("cited_by_count", "未知"))


            stats = selected_author.get("summary_stats", {})
            print("H 指数：", stats.get("h_index", "未知"))
            print("i10 指数：", stats.get("i10_index", "未知"))

#返回教授近期论文的研究方向，研究概念

            topics = selected_author.get("topics", [])
            print("\n研究方向：")
            if topics:
                for topic in topics[:5]:
                    print("-", topic.get("display_name", "未知方向"))
            else:
                print("未提供研究方向")
            keywords = selected_author.get("keywords") or []

            concepts = (
                selected_author.get("concepts")
                or selected_author.get("x_concepts")
                or []
            )

            print("\nConcept（研究概念）：")
            if concepts:
                for concept in concepts[:10]:
                    name = concept.get("display_name", "未知概念")
                    score = concept.get("score", "未知")
                    print("-", name, "｜相关度：", score)
            else:
                print("未提供 Concept 数据")

#检查教授搜索正确性.若正确，程序结束；若不正确，则循环执行教授选择

            answer = input("\n这是不是你要找的作者？(y/n)：").strip().lower()

            if answer == "y":
                print("已确认作者，程序结束。")
                break
            elif answer == "n":
                print("好的，请重新选择。")
            else:
                print("请输入 y 或 n；将返回作者列表供你重新选择。")

#用户输入的编号不存在，则循环执行教授选择

        except (ValueError, IndexError):
            print("编号无效，请输入列表中的数字。")   


