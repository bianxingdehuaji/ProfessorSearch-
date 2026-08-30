ProfessorSearch 教授信息查询

这是一个使用开源项目 PyAlex (https://github.com/J535D165/pyalex) 编写的 Python 小工具。运行后，输入教授姓名，即可从 OpenAlex 查询并选择相应教授，查看其学术资料。


**1可以做什么**

-按教授姓名搜索教授

-用所属组织缩小同名教授的范围

- 在选择列表中显示论文数量、总引用次数和所属组织

- 显示选中教授的基本资料：OpenAlex 编号、ORCID、论文总数、引用次数、H 指数和 i10 指数，显示研究方向（Topics）和研究概念（Concepts）。

-询问“这是不是你要找的教授”；输入 `y` 结束，输入 `n` 返回重新选择


*OpenAlex 中不同教授的资料完整度不同。没有机构、关键词或 Concepts 信息时，程序会显示“未提供”，这不是程序错误。*

**2运行环境**

Windows
Python 3.8 或更高版本
PyAlex
OpenAlex API key\*（需要手动配置）\*

本项目已在 Python 3.13 环境中学习和使用。

**3如何运行**

3.1安装pyalex


于powershell中输入：

python -m pip install pyalex

3.2验证安装：

于powershell中输入

python -c "from pyalex import Authors; print('PyAlex 安装成功')"

3.3配置 OpenAlex API key


3.3.1. 在 OpenAlex 官方网站(https://openalex.org/settings/api) 免费注册或登录。

3.3.2. 在 https://openalex.org/settings/api 免费创建并复制 API key。

3.3.3. 在 `ProfessorSearch.py` 顶部配置：

import pyalex
pyalex.config.api\_key = "*在这里填入你的 API 密钥*"

*只用在填入正确 API key 时，工具才能正常工作。*



*\*请勿将 API key 上传到 GitHub，也不要发送给他人。*



**4运行程序**


双击 ProfessorSearch\_CN.py 文件


程序会依次要求输入：



```

请输入教授姓名（建议使用英文）：

请输入想查看的教授编号：

这是不是你要找的教授？(y/n)：


```

建议使用英文姓名和英文机构名，例如：

\*``

教授姓名：Albert Einstein

```\*


**5一键启动***（此功能不是必须功能）*

可创建一个名为 `运行教授查询.bat` 的文件，内容如下：


```bat
@echo off
python "文件目录地址"
echo.
pause
```

以后双击该 `.bat` 文件即可启动程序；运行结束后按任意键关闭窗口。


**6常见问题**

Q:什么是OpenAlex？

A：OpenAlex（https://openalex.org/）是一个以亚历山大图书馆命名的开放获取科学论文、作者和机构书目目录。它由OurResearch于2022年1月开始运营，目前已收录超过2.5亿篇学术著作。

Q: 显示“未提供关键词”或“未提供 Concept 数据”是报错吗？

A:不是。OpenAlex 不保证每位教授都具有这些字段；研究方向（Topics）通常更常见。

Q:为什么需要 API key？

A:API key 用于识别你的 OpenAlex 账户，并提供更适合日常查询的访问额度。详见 \[PyAlex 官方文档](https://pypi.org/project/pyalex/)。

**7后续可以扩展的功能**


-查看教授被引用最多的论文

-按年份筛选教授论文

-导出教授信息到 CSV 或 Excel

-使用带输入框和按钮的图形界面

-打包为独立的 Windows `.exe` 程序


**8目前工具的不足**

\-一些重名的教授数量太多，可能无法返回所有的重名教授信息。可以考虑加入更多筛选项。

\-‘归属组织’一项准确性有限，OpenAlex数据库更新延迟可能是主要原因。

\-对于在国内发表的中文期刊支持有限。





