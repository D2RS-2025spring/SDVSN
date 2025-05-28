# DataLoaderAndCleaner.py
import pandas as pd
from tkinter import Tk, filedialog, messagebox

def load_excel_file():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择Excel文件",
        filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
    )
    if not file_path:  # 如果用户未选择文件
        messagebox.showinfo("提示", "未选择文件，程序将退出。")
        return None
    return file_path

def clean_data(df):
    df.dropna(inplace=True)  # 删除包含空值的行
    df.drop_duplicates(inplace=True)  # 删除重复的行
    return df

def save_cleaned_data(df):
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.asksaveasfilename(
        title="保存清洗后的数据",
        filetypes=[("Excel文件", "*.xlsx"), ("CSV文件", "*.csv"), ("所有文件", "*.*")],
        defaultextension=".xlsx"
    )
    if not file_path:  # 如果用户未选择保存位置
        messagebox.showinfo("提示", "未选择保存位置，清洗后的数据未保存。")
        return
    if file_path.endswith(".csv"):
        df.to_csv(file_path, index=False)  # 保存为CSV文件
    else:
        df.to_excel(file_path, index=False)  # 保存为Excel文件
    messagebox.showinfo("提示", f"清洗后的数据已保存到：{file_path}")

def main():
    print("欢迎使用数据加载与清洗工具 - DataLoaderAndCleaner")
    file_path = load_excel_file()  # 加载Excel文件
    if not file_path:
        return
    try:
        df = pd.read_excel(file_path)  # 读取Excel文件内容
        print("文件加载成功！")
    except Exception as e:
        messagebox.showerror("错误", f"加载文件时出错：{e}")
        return

    df = clean_data(df)  # 清洗数据
    print("数据清洗完成！")

    save_cleaned_data(df)  # 保存清洗后的数据
    print("程序结束。")

if __name__ == "__main__":
    main()
