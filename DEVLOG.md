ProfessorSearch 教授搜索
Github项目地址：https://github.com/bianxingdehuaji/ProfessorSearch-

这是我的第一个项目，可以用于搜索教授的影响力、近期研究方向等学术信息。这一项目利用了开源项目PyAlex (https://github.com/J535D165/pyalex) 实现功能。程序由 Codex 辅助设计。

以下是项目的开发历程。

1立项
	我在8月21日看到了物光创新实验室的招新通知，决定开始设计招新项目。
  在前一个月，我刚刚加入深大。我兴奋的在学校官网上，查询物光院的教授简介。大部分教授编辑了自己的主页，展示近期的研究。有一些教授的主页并没有完整披露，或者没有更新。官网的教授主页也没有同一标准，导致结构不一，信息混乱。
结合我想了解光电专业发展方向的需求，我想做一个工具，能够查询到教授的研究方向，方便学生了解专业产业发展趋势，和更好做出学习选择。

2项目初建
	项目开始时，我设想通过爬虫，爬取深大官网的信息，将信息作简化，以统一的格式输出。
	我在 Codex 的帮助下，完成了第一版程序：

'''

cd C:\Users\Yang\Documents\Codex\2026-08-28\wo
$env:PYTHONPATH = "src"
C:\Users\Yang\AppData\Local\Programs\Python\Python313\python.exe -m prof_researcher.cli "教授姓名" --profile-url "教授官网个人主页网址" --output-dir outputs

'''

这一版本的程序很粗糙，需要用户自己找到教授的主页，输入程序后，以文本提取的方式生成教授的简介 Markdown 文件。除非在客户端接入 AI 工具，否则我希望的研究方向，简介简化全都没有办法实现。此外，无法直接获取教授的个人简介的 URL 也是这一方案的缺点。
因此这一版本被放弃。

3现行方案
我希望能找到某一个已经被归类，整理过的数据库，这样能更好的实现期望的功能。
在一次和 ChatGPT 的对话里，我了解到了OpenAlex ，一个年轻的学术论文数据库，它向公众开放免费的 API ，供用户查询。幸运地，我在 Github 上找到了一位用户 (https://github.com/J535D165) 的公开项目 PyAlex (https://github.com/J535D165/pyalex) 。PyAlex 是一个基于 OpenAlex 的 Python 库。可以通过 PyAlex ，可以让程序调用 OpenAlex 的数据库，实现我想要的功能。
以下是第二版本的程序：

'''

from pyalex import Authors

name = input("请输入作者姓名（建议使用英文）：").strip()
authors = Authors().search(name).get(per_page=5)
if not authors:
    print("没有找到匹配的作者。请检查姓名拼写后重试。")
else:
    print("\n找到的作者：")

    for number, author in enumerate(authors, start=1):
        print("\n", number, ".", author.get("display_name", "未知姓名"))
        print("OpenAlex 编号：", author.get("id", "未知"))
        print("论文数量：", author.get("works_count", "未知"))
        print("被引用次数：", author.get("cited_by_count", "未知"))
		
'''

这一版本的程序确定了 ‘输入姓名--检索筛选--返回结果’ 的基本流程。已经具备找到教授论文数量、被引量的功能，但还需要进一步完善。
阅读了 PyAlex 的技术文档，在 Codex 的帮助下，我在检索阶段加入教授所属机构，在搜索结果加入了研究方向、影响力指标（ H 指数和 i10 指数）、关键词、概念等信息。并加入了 API key 的核验，以支持更大规模的搜索。
形成了第三版程序。

*第三版程序没有另外保存。*

测试中，我遇上了一些问题。当检索教授时，如果选择了错误的选项，程序不会有“反悔机制”，而是无论结果是否如意，都结束运行。
我在第三版的程序中加入了一个循环指令，形成第四版。

'''

 while True:

（此处是原有的第三版程序）

         if answer == "y":
                print("已确认作者，程序结束。")
                break
            elif answer == "n":
                print("好的，请重新选择。")
            else:
                print("请输入 y 或 n；将返回作者列表供你重新选择。")

'''

此时的程序已经接近最后的版本了。

4完善
	经过一些测试，我对程序进行了一些修改。
	
4.1 由于一些教授重名的数量很多，我考虑过增加教授的所属机构（ institution ），进行筛选。但是由于 OpenAlex 的数据库更新不及时，一些教授本来就没有被正确归类。于是 ‘所属机构’ 最后只被作为了选择参考，而不是必要的条件。

4.2 由于 OpenAlex 数据库对于国内教授的 ‘关键词’ 信息支持有限，大部分的教授的 ‘关键词’ 数据为空，最后删去了 ‘关键词’ 指标。

4.3 在代码中完善了注释内容，撰写 README 文档。

4.4 另外，为了方便测试，我写了一个 ‘一键运行’ 的程序。只需要双击一个 .bat 文件，程序就会自动运行。最终版本没有将其列为必要程序，参见 README 的第 5 节。
	最后项目基本完工，最终版本参见文件 ProfessorSearch_CN.py 。

5不足
	OpenAlex 对于国内发表的作者的支持有限，很多国内的学术信息更新被忽略。教授的所属机构准确性也不足。我希望可以找到内容更全面的数据库，弥补这一缺点。
	
	目前 ProfessorSearch 功能仍然局限，没有列出教授的近期文献或者代表文献的功能，输出的结果不能自动翻译成中文。程序本身没有图形化的界面，不能将结果输出到办公软件的表格。期待以后可以丰富更多功能，把 ProfessorSearch 打造成一个综合性的学术搜索平台。
	
	不过，就我最初的要求而言，ProfessorSearch 已经可以基本实现。

6结束
	在 ChatGPT ，Codex 等 AI 工具的帮助下，整一个项目消耗的时间并不多，但也让我学习到了从零开始做一个项目、解决一个问题的过程。
	
	对我来说， ProfessorSearch 也是一个我会使用的工具。

ヾ(￣▽￣)Bye~Bye~

