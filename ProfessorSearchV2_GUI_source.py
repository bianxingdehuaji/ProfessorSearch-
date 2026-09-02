import os
import json
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pyalex
from pyalex import Authors

# 配置文件保存路径（会在程序同级目录下自动生成 config.json）
CONFIG_FILE = "config.json"


class OpenAlexAuthorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ProfessorSearch 教授搜索")
        self.root.geometry("850x700")
        self.root.minsize(700, 550)

        # 存储搜索到的学者数据列表
        self.current_authors = []

        # 用于识别已取消或已被新搜索替代的后台请求
        self.search_request_id = 0

        # 建立界面控件
        self.setup_ui()

        # 程序启动时尝试从本地加载保存的 API Key
        self.load_api_key()

    def setup_ui(self):
        # ================= 0. API Key 设置区域 =================
        key_frame = ttk.LabelFrame(self.root, text=" API 设置 ", padding=10)
        key_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(key_frame, text="OpenAlex API Key:").pack(side=tk.LEFT, padx=(0, 5))

        # API Key 输入框
        self.api_key_entry = ttk.Entry(key_frame, width=40)
        self.api_key_entry.pack(side=tk.LEFT, padx=5)

        # 保存/更新按钮
        self.save_key_btn = ttk.Button(key_frame, text="保存/更新 Key", command=self.save_api_key_event)
        self.save_key_btn.pack(side=tk.LEFT, padx=5)

        # 修改按钮（用于一键解锁输入框，方便重新修改）
        self.edit_key_btn = ttk.Button(key_frame, text="修改", command=self.enable_key_editing)
        self.edit_key_btn.pack(side=tk.LEFT, padx=5)

        self.key_status_label = ttk.Label(key_frame, text="", foreground="green")
        self.key_status_label.pack(side=tk.LEFT, padx=5)

        # ================= 1. 顶部搜索框与按钮区域 =================
        search_frame = ttk.LabelFrame(self.root, text=" 教授搜索 ", padding=10)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="请输入学者姓名（建议使用英文）:").pack(side=tk.LEFT, padx=(0, 5))

        self.name_entry = ttk.Entry(search_frame, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        self.name_entry.bind("<Return>", lambda event: self.start_search())  # 回车触发搜索

        self.search_btn = ttk.Button(search_frame, text="搜索", command=self.start_search)
        self.search_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = ttk.Button(search_frame, text="清空", command=self.cancel_search)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(search_frame, text="", foreground="blue")
        self.status_label.pack(side=tk.LEFT, padx=10)

        # ================= 2. 中间区域：左侧学者列表，右侧详细信息卡片 =================
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 左侧列表框
        list_frame = ttk.LabelFrame(paned_window, text=" 匹配列表 ", padding=5)
        paned_window.add(list_frame, weight=1)

        columns = ("name", "works", "citations")
        self.author_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.author_tree.heading("name", text="姓名")
        self.author_tree.heading("works", text="论文数")
        self.author_tree.heading("citations", text="总引用")

        self.author_tree.column("name", width=120)
        self.author_tree.column("works", width=60, anchor=tk.CENTER)
        self.author_tree.column("citations", width=60, anchor=tk.CENTER)

        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.author_tree.yview)
        self.author_tree.configure(yscrollcommand=tree_scroll.set)

        self.author_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.author_tree.bind("<<TreeviewSelect>>", self.on_author_select)

        # 右侧详细信息展示文本框
        detail_frame = ttk.LabelFrame(paned_window, text=" 详细信息 ", padding=5)
        paned_window.add(detail_frame, weight=2)

        self.detail_text = tk.Text(detail_frame, wrap=tk.WORD, font=("Consolas", 10))
        text_scroll = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=self.detail_text.yview)
        self.detail_text.configure(yscrollcommand=text_scroll.set)

        self.detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    # ================= 本地 Key 配置加载/修改/保存逻辑 =================
    def load_api_key(self):
        """启动时从本地文件读取 API Key"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    api_key = config.get("api_key", "").strip()
                    if api_key:
                        self.api_key_entry.delete(0, tk.END)
                        self.api_key_entry.insert(0, api_key)
                        pyalex.config.api_key = api_key
                        
                        # 已加载成功时，输入框设为禁用（防止误触），需点击“修改”解除
                        self.api_key_entry.config(state=tk.DISABLED)
                        self.key_status_label.config(text="✓ 已加载本地 Key", foreground="green")
                        return
            except Exception as e:
                print(f"读取配置文件失败: {e}")

        # 未成功加载时保持编辑状态
        self.api_key_entry.config(state=tk.NORMAL)
        self.key_status_label.config(text="未配置 Key", foreground="red")

    def enable_key_editing(self):
        """取消输入框锁定，让用户可以随时重新编辑修改 API Key"""
        self.api_key_entry.config(state=tk.NORMAL)
        self.api_key_entry.focus_set()
        self.key_status_label.config(text="修改中...", foreground="orange")

    def save_api_key_event(self):
        """保存或更新 API Key"""
        # 如果当前是禁用状态，先解除再读取
        self.api_key_entry.config(state=tk.NORMAL)
        key = self.api_key_entry.get().strip()

        if not key:
            messagebox.showwarning("提示", "请输入有效的 API Key！")
            return

        try:
            # 覆盖更新保存到本地 json 配置文件
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"api_key": key}, f, ensure_ascii=False, indent=2)

            # 实时更新全局全局参数配置
            pyalex.config.api_key = key
            
            # 保存完成后自动锁定输入框并给出状态提示
            self.api_key_entry.config(state=tk.DISABLED)
            self.key_status_label.config(text="✓ Key 已保存/更新", foreground="green")
            messagebox.showinfo("成功", "API Key 已成功更新并保存至本地文件！")
        except Exception as e:
            messagebox.showerror("错误", f"保存 API Key 失败:\n{e}")

    # ================= 业务交互逻辑 =================
    def start_search(self):
        """发起搜索"""
        # 允许搜索前临时解除 state 以读取控件文本
        current_state = self.api_key_entry.cget("state")
        self.api_key_entry.config(state=tk.NORMAL)
        api_key = self.api_key_entry.get().strip()
        self.api_key_entry.config(state=current_state)

        if not api_key:
            messagebox.showwarning("警告", "请先填写入 API Key 并保存后再进行搜索！")
            self.enable_key_editing()
            return

        # 实时同步最新的 Key 给 pyalex
        pyalex.config.api_key = api_key

        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("提示", "请输入学者姓名！")
            return

        self.search_btn.config(state=tk.DISABLED)
        self.status_label.config(text="搜索中，请稍候...")
        self.search_request_id += 1
        request_id = self.search_request_id

        # 清空已有数据
        for item in self.author_tree.get_children():
            self.author_tree.delete(item)
        self.detail_text.delete("1.0", tk.END)

        # 异步线程搜索
        threading.Thread(target=self._async_search, args=(name, request_id), daemon=True).start()

    def cancel_search(self):
        """取消搜索并清空界面"""
        self.search_request_id += 1
        self.current_authors = []
        self.name_entry.delete(0, tk.END)
        self.status_label.config(text="")
        self.search_btn.config(state=tk.NORMAL)

        for item in self.author_tree.get_children():
            self.author_tree.delete(item)
        self.detail_text.delete("1.0", tk.END)
        self.name_entry.focus_set()

    def _async_search(self, name, request_id):
        """后台 API 查询任务"""
        try:
            authors = Authors().search(name).get(per_page=10)
            self.root.after(0, lambda: self._update_search_results(authors, request_id))
        except Exception as e:
            self.root.after(0, lambda: self._show_error(str(e), request_id))

    def _update_search_results(self, authors, request_id):
        """更新 UI 搜索列表"""
        if request_id != self.search_request_id:
            return

        self.search_btn.config(state=tk.NORMAL)
        self.status_label.config(text="")
        self.current_authors = authors or []

        if not self.current_authors:
            messagebox.showinfo("结果", "没有找到匹配的学者。请检查姓名拼写后重试。")
            return

        for index, author in enumerate(self.current_authors):
            display_name = author.get("display_name", "未知姓名")
            works_count = author.get("works_count", "未知")
            cited_by_count = author.get("cited_by_count", "未知")

            self.author_tree.insert("", tk.END, iid=index, values=(display_name, works_count, cited_by_count))

        first_item = self.author_tree.get_children()[0]
        self.author_tree.selection_set(first_item)

    def _show_error(self, err_msg, request_id):
        if request_id != self.search_request_id:
            return

        self.search_btn.config(state=tk.NORMAL)
        self.status_label.config(text="")
        messagebox.showerror("网络/API错误", f"请求发生异常，请检查网络或 API Key 是否正确:\n{err_msg}")

    def on_author_select(self, event):
        """选中列表中学者时渲染详细卡片"""
        selected_items = self.author_tree.selection()
        if not selected_items:
            return

        idx = int(selected_items[0])
        selected_author = self.current_authors[idx]

        info_text = []
        info_text.append("===== 学者基础信息 =====")
        info_text.append(f"姓名：{selected_author.get('display_name', '未知')}")
        info_text.append(f"OpenAlex 编号：{selected_author.get('id', '未知')}")
        info_text.append(f"ORCID：{selected_author.get('orcid', '未提供')}")
        info_text.append(f"论文总数：{selected_author.get('works_count', '未知')}")
        info_text.append(f"总引用次数：{selected_author.get('cited_by_count', '未知')}")

        institutions = selected_author.get("last_known_institutions") or []
        if institutions:
            inst_names = "、".join(inst.get("display_name", "未知机构") for inst in institutions[:2])
        else:
            inst_names = "未提供"
        info_text.append(f"所属组织：{inst_names}\n")

        stats = selected_author.get("summary_stats", {})
        info_text.append("===== 学术影响指数 =====")
        info_text.append(f"H 指数：{stats.get('h_index', '未知')}")
        info_text.append(f"i10 指数：{stats.get('i10_index', '未知')}\n")

        topics = selected_author.get("topics", [])
        info_text.append("===== 研究方向 (Topics) =====")
        if topics:
            for topic in topics[:10]:
                info_text.append(f"• {topic.get('display_name', '未知方向')}")
        else:
            info_text.append("未提供研究方向")
        info_text.append("")

        concepts = (
            selected_author.get("concepts")
            or selected_author.get("x_concepts")
            or []
        )
        info_text.append("===== 研究概念 (Concepts) =====")
        if concepts:
            for concept in concepts[:10]:
                c_name = concept.get("display_name", "未知概念")
                score = concept.get("score", "未知")
                info_text.append(f"• {c_name} ｜ 相关度: {score}")
        else:
            info_text.append("未提供 Concept 数据")

        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert(tk.END, "\n".join(info_text))


if __name__ == "__main__":
    root = tk.Tk()
    app = OpenAlexAuthorGUI(root)
    root.mainloop()
