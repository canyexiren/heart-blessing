import tkinter as tk
import math
import random

TEXTS = [
    "早日评上正高",
    "课题申报必中",
    "论文秒发核心",
    "公开课大获好评",
    "优质课评比一等奖",

    # --- 教学与带班日常 ---
    "带的班级断层第一",
    "学生听话不操心",
    "批改作业手不酸",
    "教案一次就过",
    "今天也没被学生气到",
    "没有晚自习的烦恼",
    "考点讲完全员秒懂",
    "高考92率起飞",

    # --- 身心关怀与教师生活 ---
    "保护嗓子多喝水",
    "拒绝内卷准时下班",
    "寒暑假快快到来",
    "放假绝不排值班",
    "烦恼通通准时下课",
    "周末睡到自然醒",

    # --- 专属甜蜜鼓励 ---
    "全世界最美的向老师",
    "累了有我给你揉肩",
    "今天下班去吃大餐",
    "天天都有好心情",
    "永远做你最强后盾"
]


# 2. 便签尺寸与马卡龙配色表（底色, 边框/字体颜色）

POPUP_W, POPUP_H = 160, 68

PALETTES = [
    ("#FFE3EC", "#C2185B"), ("#FFD6E0", "#D81B60"), ("#FFEAF1", "#AD1457"),
    ("#DFF0CE", "#2E7D32"), ("#FDE8EC", "#C62828"), ("#FFE9E0", "#E65100"),
    ("#FFF1E0", "#EF6C00"), ("#FFEDD9", "#D84315"), ("#E0F7FA", "#00838F"),
    ("#EDE7F6", "#512DA8"), ("#F3E5F5", "#6A1B9A"), ("#E8F5E9", "#1B5E20"),
    ("#FFF9C4", "#F57F17"), ("#FFF0F5", "#880E4F"), ("#E1F5FE", "#0277BD")
]

# ========================================================
# 3. 核心动画逻辑
# ========================================================
def create_popup(root, x, y, text=None):
    """创建一个圆角便签窗口"""
    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.geometry(f"{POPUP_W}x{POPUP_H}+{int(x)}+{int(y)}")

    # 尝试开启透明背景（适配 Windows 圆角效果）
    trans_color = "#000001"
    try:
        win.attributes("-transparentcolor", trans_color)
        canvas_bg = trans_color
    except Exception:
        canvas_bg = "#FFFFFF"

    bg_color, fg_color = random.choice(PALETTES)
    content = text if text else random.choice(TEXTS)

    canvas = tk.Canvas(win, width=POPUP_W, height=POPUP_H, bg=canvas_bg, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # 绘制圆角矩形
    r = 12
    pts = [
        r, 0,  POPUP_W - r, 0,
        POPUP_W, 0,  POPUP_W, r,
        POPUP_W, POPUP_H - r,  POPUP_W, POPUP_H,
        POPUP_W - r, POPUP_H,  r, POPUP_H,
        0, POPUP_H,  0, POPUP_H - r,
        0, r,  0, 0
    ]
    canvas.create_polygon(pts, smooth=True, fill=bg_color, outline=fg_color, width=1.5)
    canvas.create_text(
        POPUP_W // 2, POPUP_H // 2,
        text=content,
        fill=fg_color,
        font=("Microsoft YaHei", 10, "bold"),
        width=POPUP_W - 24,
        justify="center"
    )
    return win

def run_animation(speed=0.03):
    """
    speed: 速度控制参数（秒），数值越小动画越快
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.bind_all("<Escape>", lambda e: root.destroy())  # 按 Esc 随时退出

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()

    # 心形轨迹参数
    heart_points = []
    num_heart_notes = 75
    cx = screen_w // 2
    cy = screen_h // 2 - 20
    scale = min(screen_w, screen_h) / 54

    for i in range(num_heart_notes):
        t = math.pi - (2 * math.pi * i / num_heart_notes)
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        px = cx + scale * x - (POPUP_W // 2)
        py = cy + scale * y - (POPUP_H // 2)
        heart_points.append((px, py))

    heart_windows = []

    # 第一阶段：按心形画出便签
    def step_draw_heart(index=0):
        if index < len(heart_points):
            px, py = heart_points[index]
            win = create_popup(root, px, py)
            heart_windows.append(win)
            delay = max(5, int(speed * 1000))
            root.after(delay, lambda: step_draw_heart(index + 1))
        else:
            # 画完后停顿一小会儿，开始消除
            pause_delay = max(500, int(speed * 20000))
            root.after(pause_delay, step_shrink_heart)

    # 第二阶段：爱心便签逐渐减少
    def step_shrink_heart():
        if heart_windows:
            win = heart_windows.pop()
            win.destroy()
            delay = max(5, int(speed * 700))
            root.after(delay, step_shrink_heart)
        else:
            # 全部消除后，稍作停顿开始炸屏
            pause_delay = max(200, int(speed * 6000))
            root.after(pause_delay, step_explode)

    # 第三阶段：便签炸满屏幕
    def step_explode(count=0, total=180):
        if count < total:
            rx = random.randint(10, max(10, screen_w - POPUP_W - 10))
            ry = random.randint(10, max(10, screen_h - POPUP_H - 10))
            create_popup(root, rx, ry)
            delay = max(5, int(speed * 400))
            root.after(delay, lambda: step_explode(count + 1, total))

    root.after(100, step_draw_heart)
    root.mainloop()

run_animation(speed=0.06)