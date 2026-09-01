ProfessorSearch 教授搜索 : 教授信息查询

这是一个使用开源项目 PyAlex (https://github.com/J535D165/pyalex) 编写的 Python 小工具。运行后，输入教授姓名，即可从 OpenAlex 查询并选择相应教授，查看其学术资料。


**1可以做什么**

-按教授姓名搜索教授

-在选择列表中显示论文数量、总引用次数和所属组织

-显示选中教授的基本资料：OpenAlex 编号、ORCID、论文总数、引用次数、H 指数和 i10 指数，显示研究方向（Topics）和研究概念（Concepts）。

*OpenAlex 中不同教授的资料完整度不同。没有机构、关键词或 Concepts 信息时，程序会显示“未提供”，这不是程序错误。*




*以下内容（ 第3节和第4节 ）仅适用于 .py 文件的运行。对于打包好的 .exe 文件，不需要进行额外的配置。*

—————————————————————————————

**2运行环境**

Windows

Python 3.8 或更高版本

PyAlex

OpenAlex API key\*（需要手动配置）\*

本项目已在 Python 3.13 环境中学习和使用。

**3如何运行**

3.1安装pyalex

于powershell中输入：

```powershell
python -m pip install pyalex
```

3.2验证安装：

于powershell中输入

```powershell
python -c "from pyalex import Authors; print('PyAlex 安装成功')"

```

3.3配置 OpenAlex API key

3.3.1. 在 OpenAlex 官方网站(https://openalex.org/settings/api) 免费注册或登录。

3.3.2. 在 https://openalex.org/settings/api 免费创建并复制 API key。

3.3.3. 在 `ProfessorSearch_GUI.py` 顶部配置。程序将生成一个名为 config.json 的文件保存此密钥。


*\*请勿将 API key 上传到 GitHub，也不要发送给他人。*


**4运行程序**


双击 ProfessorSearch_GUI.py 文件


程序会要求输入：


```

请输学者姓名（建议使用英文）：


```

建议使用英文姓名，例如：

```

教授姓名：Albert Einstein


```

—————————————————————————————
**5常见问题**

Q:什么是OpenAlex？

A：OpenAlex ( https://openalex.org/ )是一个以亚历山大图书馆命名的开放获取科学论文、作者和机构书目目录。它由OurResearch于2022年1月开始运营，目前已收录超过2.5亿篇学术著作。

Q: 显示“未提供关键词”或“未提供 Concept 数据”是报错吗？

A:不是。OpenAlex 不保证每位教授都具有这些字段；研究方向（Topics）通常更常见。

Q:为什么需要 API key？

A:API key 用于识别你的 OpenAlex 账户，并提供更适合日常查询的访问额度。详见 \[PyAlex 官方文档] ( https://pypi.org/project/pyalex/ )。

Q:程序返回的‘研究方向 ( Topics ) ’ 和 ‘研究概念 ( Concepts ) ’ 是依据什么得出的？

A:研究方向 ( Topics ) : OpenAlex 先依据论文之间的引用关系构建主题群，再用模型读取每篇论文的标题、摘要、引用和期刊信息，为论文分配最多 3 个主题；作者的 Topics 则汇总其论文最常出现的主题并排序。新论文被收录后，作者的主题计数和排序可能变化。
研究概念 ( Concepts ) : OpenAlex 的旧系统基于 Microsoft Academic Graph，用模型根据论文标题、摘要等资料生成概念和相关度分数。不是“最近研究”的指标；它已停止维护，结果不会持续重新计算。

**6后续可以扩展的功能**


-查看教授被引用最多的论文

-按年份筛选教授论文

-导出教授信息到 CSV 或 Excel

-用户的搜索记录


**7目前工具的不足**

\-一些重名的教授数量太多，可能无法返回所有的重名教授信息。可以考虑加入更多筛选项。

\-‘归属组织’一项准确性有限，OpenAlex数据库更新延迟可能是主要原因。

\-对于在国内发表的中文期刊支持有限。


**8开源项目引用和 AI 辅助声明**

8.1本项目使用了 OpenAI Codex 辅助开发。

8.2本项目使用以下公开数据和开源项目：

- OpenAlex：提供学术作者、论文及研究主题数据
  https://openalex.org/
  
- PyAlex：OpenAlex API 的 Python 客户端
 https://github.com/J535D165/pyalex
  

感谢相关开源社区提供的数据与工具支持。
