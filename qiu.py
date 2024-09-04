import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Script(src="https://d3js.org/d3.v6.min.js"),  # 加载D3.js库
    html.Div(id="globe-container"),  # 用于渲染D3可视化的容器
    html.Script(src="/assets/globe.js")  # 加载你的自定义D3.js代码
])

if __name__ == '__main__':
    app.run_server(debug=True)
