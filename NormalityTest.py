# NormalityTest.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from tkinter import Tk, filedialog, messagebox, simpledialog
from scipy.stats import skew, kurtosis

# 设置字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 定义函数：绘制箱线图
def plot_boxplot(df, column, unit=None):
    plt.figure(figsize=(8, 6))
    plt.boxplot(df[column].dropna())
    plt.title(f'Boxplot of {column} ({unit})')
    plt.ylabel(f'{column} ({unit})')
    plt.show()

# 其他代码保持不变

# Implementing smirnov_grubbs function
def smirnov_grubbs(data, alpha=0.05):
    n = len(data)
    if n < 3:
        return None  # Grubbs' test requires at least 3 data points
    
    mean = np.mean(data)
    std_dev = np.std(data, ddof=1)
    max_deviation = max(abs(x - mean) for x in data)
    G = max_deviation / std_dev
    
    # Calculate the critical value for Grubbs' test
    t_alpha_over_2n = stats.t.ppf(1 - alpha / (2 * n), n - 2)
    G_critical = ((n - 1) / np.sqrt(n)) * np.sqrt((t_alpha_over_2n ** 2) / (n - 2 + t_alpha_over_2n ** 2))
    
    if G > G_critical:
        outlier_index = np.argmax([abs(x - mean) for x in data])
        return outlier_index
    return None

# 设置字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 定义函数：加载用户选择的Excel文件
def load_excel_file():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择清洗后的文件",
        filetypes=[("Excel文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
    )
    if not file_path:  # 如果用户未选择文件
        messagebox.showinfo("提示", "未选择文件，程序将退出。")
        return None
    return file_path

# 定义函数：清洗数据（删除空值和重复值）
def clean_data(df):
    df.dropna(inplace=True)  # 删除包含空值的行
    df.drop_duplicates(inplace=True)  # 删除重复的行
    return df

# 定义函数：进行正态性检验
def normality_test(df):
    results = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):  # 确保列是数值类型
            skewness = skew(df[col], bias=False)
            kurtosis_value = kurtosis(df[col], bias=False)
            normal = abs(skewness) <= 1.96 and abs(kurtosis_value - 3) <= 1.96  # 判断是否为正态分布
            results[col] = {
                'Skewness': skewness,
                'Kurtosis': kurtosis_value,
                'Normal': normal,
                'Outliers': []  # 初始化异常值列表
            }
    return results

# 定义函数：使用GRUBBS检验法进行异常值判别
def grubbs_test(df, column, alpha=0.05):
    outliers_removed = smirnov_grubbs(df[column].values, alpha=alpha)
    return outliers_removed

# 定义函数：使用DIXON检验法进行异常值判别
def dixon_test(df, column, alpha=0.05):
    data = df[column].dropna().values
    n = len(data)
    
    if n < 3:
        return None  # Dixon's test requires at least 3 data points
    
    # Sort the data
    sorted_data = np.sort(data)
    
    # Define critical values for alpha = 0.05
    critical_values = {
        3: 0.941,
        4: 0.765,
        5: 0.642,
        6: 0.560,
        7: 0.507,
        8: 0.468,
        9: 0.437,
        10: 0.412
    }
    
    if n not in critical_values:
        return None  # Critical value not defined for this sample size
    
    Q_critical = critical_values[n]
    
    # Calculate Q for the smallest and largest value
    Q1 = (sorted_data[1] - sorted_data[0]) / (sorted_data[-1] - sorted_data[0])
    Qn = (sorted_data[-1] - sorted_data[-2]) / (sorted_data[-1] - sorted_data[0])
    
    Q = max(Q1, Qn)
    
    if Q > Q_critical:
        if Q == Q1:
            return [sorted_data[0]]
        elif Q == Qn:
            return [sorted_data[-1]]
    
    return None

# 定义函数：自动进行异常值判别，直至没有异常值
def auto_outlier_detection(df, sample_column):
    results = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):  # 确保列是数值类型
            results[col] = []
            while True:
                out_idx_grubbs = grubbs_test(df, col, alpha=0.05)
                out_idx_dixon = dixon_test(df, col, alpha=0.05)
                out_idx = out_idx_grubbs or out_idx_dixon
                if out_idx is not None:
                    results[col].append(out_idx)
                    df = df.drop(df.index[out_idx])
                else:
                    break
    return results

# 主程序
def main():
    print("欢迎使用正态性检验与异常值判别工具 - NormalityAndOutlierDetection")
    file_path = load_excel_file()  # 加载Excel文件
    if not file_path:
        return None
    try:
        df = pd.read_excel(file_path)  # 读取Excel文件内容
        print("文件加载成功！")
    except Exception as e:
        print(f"加载文件时出错：{e}")
        return None

    df = clean_data(df)  # 清洗数据
    print("数据清洗完成！")

    normality_results = normality_test(df)  # 进行正态性检验
    print("正态性检验结果：")
    for col, stats in normality_results.items():
        print(f"{col}: Skewness={stats['Skewness']:.4f}, Kurtosis={stats['Kurtosis']:.4f}, "
              f"Normal={stats['Normal']}")

    # 假设单位信息存储在一个字典中
    units = {'pH': '无', '砷': 'mg/L', '汞': 'mg/L', '硒': 'mg/L', '铍': 'mg/L',
             '钒': 'mg/L', '锰': 'mg/L', '钴': 'mg/L', '锑': 'mg/L', '镍': 'mg/L',
             '铬': 'mg/L', '铜': 'mg/L', '锌': 'mg/L', '镉': 'mg/L', '铅': 'mg/L'}

    for col, stats in normality_results.items():
        if not stats['Normal']:  # 如果数据不是正态分布，绘制箱线图
            plot_boxplot(df, col, unit=units.get(col, '无'))

    root = Tk()
    root.withdraw()  # 隐藏主窗口
    sample_column = simpledialog.askstring("输入", "请输入样品名称列的名称：", parent=root)
    if not sample_column:
        messagebox.showinfo("提示", "未输入样品名称列，程序将退出。")
        return None

    outlier_results = auto_outlier_detection(df.copy(), sample_column)  # 自动进行异常值判别
    print("异常值判别结果：")
    for col, outliers in outlier_results.items():
        for outlier in outliers:
            sample_name = df.loc[outlier, sample_column]  # 获取样品名称
            print(f"{col} 异常值索引：{outlier}, 样品名称：{sample_name}")
            normality_results[col]['Outliers'].append(sample_name)  # 将异常值记录到结果中

    return normality_results  # 返回正态性检验和异常值结果

if __name__ == "__main__":
    main()
