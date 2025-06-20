# DataLoaderAndCleaner.py
import pandas as pd
import os


def load_excel_file(default_file_path="example.xlsx"):
    user_input = input(f"请输入Excel文件路径 (默认为 {default_file_path}): ").strip()
    
    file_path = user_input if user_input else default_file_path
    
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在。请提供一个有效的文件路径。")
        return None
    return file_path

def clean_data(df):
    df.dropna(inplace=True)  # 删除包含空值的行
    df.drop_duplicates(inplace=True)  # 删除重复的行
    return df

def save_cleaned_data(df, default_save_path="cleaned_data.xlsx"):
    user_input = input(f"请输入保存清洗后数据的路径 (默认为 {default_save_path}): ").strip()
    file_path = user_input if user_input else default_save_path

    if not file_path:
        print("未选择保存位置，清洗后的数据未保存。")
        return

    try:
        if file_path.endswith(".csv"):
            df.to_csv(file_path, index=False)  # 保存为CSV文件
        else:
            # Ensure directory exists for the output file
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            df.to_excel(file_path, index=False)  # 保存为Excel文件
        print(f"清洗后的数据已保存到：{file_path}")
    except Exception as e:
        print(f"错误: 保存文件时出错：{e}")

def main():
    print("欢迎使用数据加载与清洗工具 - DataLoaderAndCleaner")
    file_path = load_excel_file()  # 加载Excel文件
    if not file_path:
        return
    try:
        df = pd.read_excel(file_path)  # 读取Excel文件内容
        print("文件加载成功！")
    except Exception as e:
        print(f"错误: 加载文件时出错：{e}")
        return

    df = clean_data(df)  # 清洗数据
    print("数据清洗完成！")

    save_cleaned_data(df)  # 保存清洗后的数据
    print("程序结束。")

if __name__ == "__main__":
    main()
