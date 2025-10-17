MAIN_COLOR = "#008080"
LIGHT_BG = "#ffffff"
ADMIN_BG = "#004d4d"

def button_style(bg=MAIN_COLOR, color="white"):
    return f"""
        QPushButton{{background:{bg};color:{color};border-radius:8px;padding:8px;font-weight:600;}}
        QPushButton:hover{{background:#006666;}}
    """
