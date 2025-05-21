import pandas as pd
from DataLoaderAndCleaner import main as load_clean_main
from NormalityTest import main as normality_main
from VisualizationGraph import main as visualization_main

def generate_html_report():
    # 运行数据加载与清洗模块
    load_clean_main()
    
    # 运行正态性检验与异常值判别模块
    normality_results = normality_main()
    
    if normality_results is None:
        print("正态性检验模块未返回结果，无法生成报告。")
        return
    
    # 运行数据可视化模块
    visualization_main()
    
    # 创建HTML报告内容
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>数据分析全流程分析报告</title>
        <style>
            body {{
                font-family: SimHei, sans-serif; /* 使用黑体字体 */
                line-height: 1.6;
                margin: 20px;
            }}
            h1, h2, h3 {{
                color: #333;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
            }}
            .section {{
                margin-bottom: 20px;
            }}
            .chart {{
                /* 移除宽度和高度限制，确保图片按原始比例显示 */
                max-width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            table, th, td {{
                border: 1px solid #ddd;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>数据分析全流程分析报告</h1>
            <p>日期：2025年05月21日</p>
            
            <!-- 数据加载与清洗模块 -->
            <div class="section">
                <h2>一、数据加载与清洗</h2>
                <p>加载用户选择的Excel文件，删除空值和重复值，并保存清洗后的数据。</p>
                <table>
                    <tr>
                        <th>步骤</th>
                        <th>操作</th>
                        <th>结果</th>
                    </tr>
                    <tr>
                        <td>1</td>
                        <td>加载Excel文件</td>
                        <td>成功加载文件</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>删除空值</td>
                        <td>删除了X行空值</td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>删除重复值</td>
                        <td>删除了Y行重复值</td>
                    </tr>
                    <tr>
                        <td>4</td>
                        <td>保存清洗后的数据</td>
                        <td>保存到指定路径</td>
                    </tr>
                </table>
            </div>
            
            <!-- 正态性检验与异常值判别模块 -->
            <div class="section">
                <h2>二、正态性检验与异常值判别</h2>
                <p>对数据进行正态性检验，并使用Grubbs和Dixon检验法识别异常值。</p>
                <table>
                    <tr>
                        <th>指标</th>
                        <th>偏度 (Skewness)</th>
                        <th>峰度 (Kurtosis)</th>
                        <th>是否正态</th>
                        <th>异常值</th>
                    </tr>
                    {"".join([f"<tr><td>{col}</td><td>{stats['Skewness']:.2f}</td><td>{stats['Kurtosis']:.2f}</td><td>{'是' if stats['Normal'] else '否'}</td><td>{stats.get('Outliers', '无')}</td></tr>" for col, stats in normality_results.items()])}
                </table>
            </div>
            
            <!-- 数据可视化模块 -->
            <div class="section">
                <h2>三、数据可视化</h2>
                <p>绘制雷达图、污染指数玫瑰图、直方图、相关性热力图等。</p>
                <h3>1. 雷达图</h3>
                <img src="radar_chart.png" class="chart">
                <h3>2. 污染指数玫瑰图</h3>
                <img src="rose_chart.png" class="chart">
                <h3>3. 直方图</h3>
                <img src="histogram_chart.png" class="chart">
                <h3>4. 相关性热力图</h3>
                <img src="heatmap_chart.png" class="chart">
                <h3>5. 随机森林特征重要性图</h3>
                <img src="feature_importance_chart.png" class="chart">
            </div>
            
            <!-- 分析结果总结 -->
            <div class="section">
                <h2>四、分析结果总结</h2>
                <p>根据上述分析，我们可以得出以下结论：</p>
                <ul>
                    <li>数据经过清洗后，质量得到了显著提升。</li>
                    <li>部分指标不符合正态分布，需要进一步分析。</li>
                    <li>通过可视化图表，我们可以直观地看到各指标的分布和相关性。</li>
                </ul>
                <p>建议：根据分析结果，进一步优化数据处理流程，并对异常值进行深入调查。</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # 保存HTML文件
    with open("data_analysis_report.html", "w", encoding="utf-8") as file:
        file.write(html_content)

if __name__ == "__main__":
    generate_html_report()