from dash import html, dcc, Input, Output, State
import dash

# 假设有10张图片，生成路径为 '/assets/sticklmgs/00001.png' 至 '/assets/sticklmgs/00010.png'
image_paths = [f'/assets/sticklmgs/{i:05d}.png' for i in range(1, 11)]

def generate_image_sequence():
    return html.Div(style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'flex-direction': 'column',
        'width': '100vw',
        'height': '100vh',
        'overflow': 'hidden'  # 防止出现滚动条
    }, children=[
        html.Div(style={'flex-grow': '1', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}, children=[
            html.Img(id='image-sequence', src=image_paths[0], style={
                'max-width': '100%',
                'max-height': '100%',
                'height': 'auto',
                'margin': 'auto',
                'object-fit': 'contain'  # 保持图片比例
            })
        ]),
        html.Div(style={
            'display': 'flex',
            'justify-content': 'center',
            'align-items': 'center',
            'width': '100%',
            'padding': '10px'
        }, children=[
            html.Button("暂停", id="pause-button", n_clicks=0),
            html.Div(style={'flex-grow': '1', 'margin-left': '20px'}, children=[
                dcc.Slider(
                    id='image-slider',
                    min=0,
                    max=len(image_paths) - 1,
                    step=1,
                    value=0,
                    marks={i: str(i + 1) for i in range(len(image_paths))},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ])
        ]),
        dcc.Interval(
            id='interval-component',
            interval=1000,  # 1秒钟
            n_intervals=0
        )
    ])

def generate_main_page(selected_data):
    content = []

    # 只展示时序图片
    if selected_data['level-1'] == '海冰' and selected_data['level-2'] == '高排放':
        content.append(generate_image_sequence())
    elif selected_data['level-1'] == '植被' and selected_data['level-2'] == '树':
        content.append(generate_image_sequence())

    # 设置整个页面的居中显示
    return html.Div(content, style={
        'display': 'flex',
        'justify-content': 'center',
        'align-items': 'center',
        'width': '100vw',
        'height': '100vh'
    })

# 添加暂停/播放功能
@dash.callback(
    Output('interval-component', 'interval'),
    Input('pause-button', 'n_clicks'),
    State('interval-component', 'interval')
)
def pause_play_button(n_clicks, current_interval):
    if n_clicks is None:
        n_clicks = 0

    if n_clicks % 2 == 1:
        return 86400000  # 设置为一天，基本等同于暂停
    return 1000  # 继续播放，每秒切换一次图片
