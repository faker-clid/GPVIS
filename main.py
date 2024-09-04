import json
from dash import Dash, html, no_update, ALL, dcc
from dash.dependencies import Input, Output, State
from dash import callback_context
from main_page import generate_main_page, image_paths

# 读取 JSON 文件
with open('btnConfig.json', 'r', encoding='utf-8') as f:
    btn_config = json.load(f)

# 初始化 Dash 应用，允许忽略回调异常
app = Dash(__name__, suppress_callback_exceptions=True)

# 生成按钮
def generate_button(button_item, button_id, active=False):
    button_class = 'button active' if active else 'button'
    img_class = 'nav-icon' + (' blue-background' if active else '')
    
    return html.Button(
        children=[
            html.Img(src=f'assets/{button_item.get("icon", "default.png")}', className=img_class),
            html.Div(button_item.get('label', ''), className='nav-text')
        ],
        id=button_id,
        n_clicks=0,
        className=button_class
    )

def init_layout(config):
    # 生成第一级按钮（海冰、植被等）
    first_level_buttons = [generate_button(item, {'type': 'level-1-button', 'index': i}, active=(i == 0)) for i, item in enumerate(config['btnConfigList'])]

    return html.Div(style={
        'width': '100vw',
        'height': '100vh',
        'position': 'relative'  # 使用相对定位，让按钮和图片位置独立
    }, children=[
        # 左侧按钮区域
        html.Div(style={
            'position': 'absolute',  # 绝对定位，使按钮区域固定在左侧
            'top': '50px',  # 距离顶部一定距离
            'left': '10px',  # 距离左侧一定距离
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'flex-start',  # 左对齐
            'justify-content': 'flex-start',
            'width': '15vw',  # 固定宽度，按钮区域不会影响图片居中
        }, children=[
            dcc.Store(id='selected-store', data={'level-1': None, 'level-2': None, 'level-3': None}),  # 添加 selected-store
            html.Div(id='level-1-container', children=first_level_buttons, style={
                'display': 'flex', 
                'flex-direction': 'row',  # 按钮水平排列
                'flex-wrap': 'wrap',  # 自动换行
                'margin-bottom': '10px'
            }),
            html.Div(id='level-2-container', style={
                'display': 'flex', 
                'flex-direction': 'row',  # 按钮水平排列
                'flex-wrap': 'wrap',  # 自动换行
                'margin-bottom': '10px'
            }),
            html.Div(id='level-3-container', style={
                'display': 'flex', 
                'flex-direction': 'row',  # 按钮水平排列
                'flex-wrap': 'wrap',  # 自动换行
                'margin-bottom': '10px'
            })
        ]),
        
        # 主内容区域
        html.Div(id='main-page-container', style={
            'display': 'flex',
            'flex-direction': 'column',
            'align-items': 'center',
            'justify-content': 'center',  # 水平和垂直方向居中
            'width': '100vw',
            'height': '100vh',
            'margin': '0 auto'
        }, children=[
            html.H1("请选择分析项", style={'text-align': 'center', 'margin-top': '20px'})
        ])
    ])








app.layout = init_layout(btn_config)

# 回调：更新图片和进度条
@app.callback(
    [Output('image-sequence', 'src'),
     Output('image-slider', 'value')],
    [Input('interval-component', 'n_intervals'),
     Input('image-slider', 'value')],
    [State('image-slider', 'value')]
)
def update_image(n_intervals, slider_value, current_value):
    ctx = callback_context
    if not ctx.triggered:
        return no_update, no_update
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'interval-component':
        new_value = (current_value + 1) % len(image_paths)
    elif triggered_id == 'image-slider':
        new_value = slider_value
    else:
        new_value = current_value

    return image_paths[new_value], new_value

# 回调：更新按钮显示和存储选择的按钮
@app.callback(
    [Output('level-1-container', 'children'),
     Output('level-2-container', 'children'),
     Output('level-3-container', 'children'),
     Output('main-page-container', 'children'),  # 主页面内容
     Output('selected-store', 'data')],
    [Input({'type': 'level-1-button', 'index': ALL}, 'n_clicks'),
     Input({'type': 'level-2-button', 'index': ALL}, 'n_clicks'),
     Input({'type': 'level-3-button', 'index': ALL}, 'n_clicks')],
    [State('level-1-container', 'children'),
     State('level-2-container', 'children'),
     State('level-3-container', 'children'),
     State('selected-store', 'data')]
)
def update_buttons(level_1_clicks, level_2_clicks, level_3_clicks, level_1_children, level_2_children, level_3_children, selected_data):
    ctx = callback_context
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update

    # 提取触发的按钮ID信息
    triggered_id = ctx.triggered[0]['prop_id']
    triggered_index = eval(triggered_id.split('.')[0])['index']

    if 'level-1-button' in triggered_id:
        selected_item = btn_config['btnConfigList'][triggered_index]
        siblings = btn_config['btnConfigList']
        selected_data['level-1'] = selected_item['label']
        selected_data['level-2'] = None
        selected_data['level-3'] = None
        buttons = [generate_button(item, {'type': 'level-1-button', 'index': i}, active=(i == triggered_index)) for i, item in enumerate(siblings)]
        if 'child' in selected_item:
            second_level_buttons = [generate_button(item, {'type': 'level-2-button', 'index': i}) for i, item in enumerate(selected_item['child'])]
            main_page_content = generate_main_page(selected_data)  # 生成主页面内容
            return buttons, second_level_buttons, [], main_page_content, selected_data
        main_page_content = generate_main_page(selected_data)  # 生成主页面内容
        return buttons, [], [], main_page_content, selected_data

    if 'level-2-button' in triggered_id:
        parent_index = next((i for i, btn in enumerate(level_1_children) if 'active' in btn['props']['className']), None)
        parent_item = btn_config['btnConfigList'][parent_index]
        selected_item = parent_item['child'][triggered_index]
        siblings = parent_item['child']
        selected_data['level-2'] = selected_item['label']
        selected_data['level-3'] = None
        buttons = [generate_button(item, {'type': 'level-2-button', 'index': i}, active=(i == triggered_index)) for i, item in enumerate(siblings)]
        if 'child' in selected_item:
            third_level_buttons = [generate_button(item, {'type': 'level-3-button', 'index': i}) for i, item in enumerate(selected_item['child'])]
            main_page_content = generate_main_page(selected_data)  # 生成主页面内容
            return no_update, buttons, third_level_buttons, main_page_content, selected_data
        main_page_content = generate_main_page(selected_data)  # 生成主页面内容
        return no_update, buttons, [], main_page_content, selected_data

    if 'level-3-button' in triggered_id:
        parent_index = next((i for i, btn in enumerate(level_2_children) if 'active' in btn['props']['className']), None)
        parent_item = next(item for item in btn_config['btnConfigList'] if item['label'] == selected_data['level-1'])
        selected_item = parent_item['child'][parent_index]['child'][triggered_index]
        siblings = parent_item['child'][parent_index]['child']
        selected_data['level-3'] = selected_item['label']
        buttons = [generate_button(item, {'type': 'level-3-button', 'index': i}, active=(i == triggered_index)) for i, item in enumerate(siblings)]
        main_page_content = generate_main_page(selected_data)  # 生成主页面内容
        return no_update, no_update, buttons, main_page_content, selected_data

    return no_update, no_update, no_update, no_update, no_update

if __name__ == '__main__':
    app.run_server(debug=True)
