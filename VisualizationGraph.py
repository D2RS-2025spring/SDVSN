import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import Tk, filedialog, messagebox
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 设置 Matplotlib 使用黑体字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用于显示负号

# 用户上传数据文件
def load_data():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择数据文件",
        filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
    )
    if not file_path:  # 如果用户未选择文件
        messagebox.showinfo("提示", "未选择文件，程序将退出。")
        return None
    try:
        data = pd.read_excel(file_path)
        print("文件加载成功！")
        return data
    except Exception as e:
        messagebox.showerror("错误", f"加载文件时出错：{e}")
        return None

# 绘制雷达图（每个指标一个雷达图，共用一个图）
def plot_radar_chart(data):
    columns = ['砷', '汞', '硒', '铍', '钒', '锰', '钴', '锑', '镍', '铬', '铜', '锌', '镉', '铅']
    labels = np.array(columns)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # 闭合图形

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title('各指标雷达图', size=20, color='blue', y=1.1)

    for i, col in enumerate(columns):
        data_radar = [data[col].mean()] * len(labels)  # 使用平均值
        data_radar += data_radar[:1]  # 闭合图形
        ax.plot(angles, data_radar, label=col, linewidth=1)
        ax.fill(angles, data_radar, alpha=0.1)

    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig("radar_chart.png")  # 保存图表为图片
    plt.close()

# 绘制污染指数玫瑰图（每个指标一个玫瑰图，共用一个图）
def plot_rose_chart(data):
    columns = ['砷', '汞', '硒', '铍', '钒', '锰', '钴', '锑', '镍', '铬', '铜', '锌', '镉', '铅']
    labels = np.array(columns)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # 闭合图形

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title('各指标污染指数玫瑰图', size=20, color='blue', y=1.1)

    for i, col in enumerate(columns):
        data_rose = [data[col].mean()] * len(labels)  # 使用平均值
        data_rose += data_rose[:1]  # 闭合图形
        ax.bar(angles, data_rose, width=0.4, label=col, alpha=0.5)

    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig("rose_chart.png")  # 保存图表为图片
    plt.close()

