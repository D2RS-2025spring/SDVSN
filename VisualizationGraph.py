
# 绘制直方图
def plot_histogram(data):
    columns = ['砷', '汞', '硒', '铍', '钒', '锰', '钴', '锑', '镍', '铬', '铜', '锌', '镉', '铅']
    data_hist = data[columns]

    fig, axes = plt.subplots(nrows=4, ncols=4, figsize=(20, 20))
    axes = axes.flatten()
    for i, col in enumerate(columns):
        sns.histplot(data_hist[col], kde=True, ax=axes[i])
        axes[i].set_title(f'{col} 分布')
    plt.tight_layout()
    plt.savefig("histogram_chart.png")  # 保存图表为图片
    plt.close()

# 绘制相关性热力图
def plot_correlation_heatmap(data):
    columns = ['砷', '汞', '硒', '铍', '钒', '锰', '钴', '锑', '镍', '铬', '铜', '锌', '镉', '铅']
    data_corr = data[columns].corr()

    plt.figure(figsize=(12, 10))
    sns.heatmap(data_corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    plt.title('指标相关性热力图', size=20)
    plt.savefig("heatmap_chart.png")  # 保存图表为图片
    plt.close()

# 绘制随机森林模型的特征重要性图
def plot_random_forest_feature_importance(data):
    columns = ['砷', '汞', '硒', '铍', '钒', '锰', '钴', '锑', '镍', '铬', '铜', '锌', '镉', '铅']
    X = data[columns]
    y = data['pH']  # 假设目标变量是 pH 值

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练随机森林模型
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 预测并计算均方误差
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f'随机森林模型的均方误差 (MSE): {mse:.2f}')

    # 绘制特征重要性图
    feature_importances = model.feature_importances_
    feature_names = columns

    plt.figure(figsize=(12, 8))
    sns.barplot(x=feature_importances, y=feature_names, palette='viridis')
    plt.title('随机森林模型的特征重要性', size=20)
    plt.xlabel('重要性')
    plt.ylabel('特征')
    plt.savefig("feature_importance_chart.png")  # 保存图表为图片
    plt.close()

# 绘制小提琴图
def plot_violin_plot(data):
    columns = ['砷', '汞', '硒', '铍', '钒', '锰', '钴', '锑', '镍', '铬', '铜', '锌', '镉', '铅']
    data_violin = data[columns]

    plt.figure(figsize=(15, 10))
    sns.violinplot(data=data_violin, palette='viridis')
    plt.title('各指标小提琴图', size=20)
    plt.xlabel('指标')
    plt.ylabel('值')
    plt.savefig("violin_chart.png")  # 保存图表为图片
    plt.close()

# 主函数
def main():
    data = load_data()
    if data is None:
        return

    plot_radar_chart(data)
    plot_rose_chart(data)
    plot_histogram(data)
    plot_correlation_heatmap(data)
    plot_random_forest_feature_importance(data)
    plot_violin_plot(data)

if __name__ == "__main__":
    main()
