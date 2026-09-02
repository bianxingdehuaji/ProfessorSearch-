# ProfessorSearchV2 教授搜索V2

Github项目地址：https://github.com/bianxingdehuaji/ProfessorSearch-

ProfessorSearch是我的第一个项目，可以用于搜索教授的影响力、近期研究方向等学术信息。这一项目利用了开源项目PyAlex (https://github.com/J535D165/pyalex) 实现功能。项目使用了 ChatGPT、Codex 等 AI 工具进行资料检索与辅助开发。项目的需求定义、方案选择、测试与迭代由我持续参与完成。

ProfessorSearchV2 是ProfessorSearchV1 的迭代版本。V2 在 V1 的基础功能不变的前提下，进行了底层的重构，新增了图形化的 UI ，并完成了打包封装。V2 目前更接近项目的实际模式，不需要额外配置即可使用。

以下是 ProfessorSearchV2 的开发历程：

1 ProfessorSearchV1功能基本实现

经过测试，ProfessorSearchV1 的功能达成预期，但是易用性方面存在以下问题：

-需要额外配置 python 环境，安装Pyalex 的数据库。
-需要用户自行编辑 API 密钥。
-没有图形化的 UI 。
-程序稳定性不足，不能保护程序不被更改。
-没有设计多次搜索的机制：启动一次程序，只能搜集一个教授的信息。

因此，我进一步开发了 ProfessorSearchV2 ，完善 V1 存在的问题。

2 ProfessorSearch 底层重构

因为我个人对于 GUI 的编写没有经验，ProfessorSearch 的 GUI 编写全部由 AI 完成。

利用 python 的 tkinter 功能，ProfessorSearch 的图形化基本完成。形成 V2 的第一版程序。

为了能顺利搜索，ProfessorSearch 需要使用用户在 OpenAlex 的私人 API 密钥。因此，为了达成封装运行的目标，程序必须能接受用户的 API 密钥输入。

在第二版的程序中，我尝试加入了一个额外的输入框，专门用来输入用户的 API 密钥。但是，用户每一次搜索都必须输入一次密钥，显然是不合理的，因此考虑另一种方案：生成一个本地文件，长期保存密钥。

在第一版的基础上，程序加入了一个 API 密钥本地化保存的机制。第三版的新增变化如下：


'''

以上是第一版程序

CONFIG_FILE = "config.json"

#配置文件保存路径（会在程序同级目录下自动生成 config.json）

self.load_api_key()

#程序启动时尝试从本地加载保存的 API Key

key_frame = ttk.LabelFrame(self.root, text=" API 设置 ", padding=10) key_frame.pack(fill=tk.X, padx=10, pady=5)

ttk.Label(key_frame, text="OpenAlex API Key:").pack(side=tk.LEFT, padx=(0, 5))

#显示API Key 输入框 

self.api_key_entry = ttk.Entry(key_frame, width=45) self.api_key_entry.pack(side=tk.LEFT, padx=5)

self.save_key_btn = ttk.Button(key_frame, text="保存 Key",command=self.save_api_key_event) 

#将密钥保存在本地

self.save_key_btn.pack(side=tk.LEFT, padx=5) 

self.key_status_label = ttk.Label(key_frame, text="", foreground="green") self.key_status_label.pack(side=tk.LEFT, padx=5)

以下是第一版程序

'''

经过测试，第三版程序有一个硬伤：密钥一经保存就不能更改。为了修复问题，第四版更改了第三版的新增部分，如下：

'''
key_frame = ttk.LabelFrame(self.root, text=" API 设置 ", padding=10)
key_frame.pack(fill=tk.X, padx=10, pady=5)

ttk.Label(key_frame, text="OpenAlex API Key:").pack(side=tk.LEFT, padx=(0, 5))

#API Key 输入框

self.api_key_entry = ttk.Entry(key_frame, width=40)
self.api_key_entry.pack(side=tk.LEFT, padx=5)

#保存/更新按钮

self.save_key_btn = ttk.Button(key_frame, text="保存/更新 Key", command=self.save_api_key_event)
self.save_key_btn.pack(side=tk.LEFT, padx=5)

#修改按钮（用于一键解锁输入框，方便重新修改）

self.edit_key_btn = ttk.Button(key_frame, text="修改", command=self.enable_key_editing)
self.edit_key_btn.pack(side=tk.LEFT, padx=5)

self.key_status_label = ttk.Label(key_frame, text="", foreground="green")
self.key_status_label.pack(side=tk.LEFT, padx=5)

'''

经过测试， API 密钥可以在第四版中正确保存并修改。至此，程序完成了封装之前的准备。

3封装

通过打包工具 pyinstaller ，程序被打包为 ProfessorSearch_GUI.exe。通过测试，所用功能运行稳定。封装完成

撰写 README 后，ProfessorSearchV2 被命名为 ProfessorSearch_GUI 上传到 GitHub。

4展望

顺利的图形化和封装极大的降低了使用门槛，但是，和 V1 一样，很多功能还没有被完善：
	- OpenAlex 数据库对国内学者的支持有限，一些数据更新延迟。
	-未来可以拓展：用户搜索记录，结果输出为CSV 和 Excel 表格，展示教授的代表文章等功能。

 

