def get_stylesheet(is_dark: bool = True) -> str:
    # Pro Seviyesi Mor/Yakut (Purple/Ruby) Accent Renkleri (Catppuccin Mocha / Latte ilhamlı)
    accent = "#cba6f7" if is_dark else "#8839ef"
    accent_hover = "#b4befe" if is_dark else "#7287fd"
    accent_pressed = "#f5c2e7" if is_dark else "#ea76cb"
    
    danger = "#f38ba8" if is_dark else "#d20f39"
    danger_hover = "#eba0ac" if is_dark else "#e64553"
    
    bg_main = "#1e1e2e" if is_dark else "#eff1f5"
    bg_panel = "#181825" if is_dark else "#e6e9ef"
    bg_item = "#313244" if is_dark else "#ccd0da"
    bg_item_hover = "#45475a" if is_dark else "#bcc0cc"
    
    border_color = "#313244" if is_dark else "#ccd0da"
    text_main = "#cdd6f4" if is_dark else "#4c4f69"
    text_dim = "#a6adc8" if is_dark else "#6c6f85"
    
    return f"""
    QMainWindow {{
        background-color: {bg_main};
        color: {text_main};
    }}
    QWidget {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
        font-size: 13px;
        color: {text_main};
    }}
    
    /* Top Bar */
    QWidget#TopBar {{
        background-color: {bg_panel};
        border-bottom: 2px solid {border_color};
    }}

    /* Sidebar */
    QListWidget#Sidebar {{
        background-color: {bg_panel};
        border: none;
        border-right: 1px solid {border_color};
        color: {text_dim};
        font-size: 14px;
        padding: 10px 5px;
    }}
    QListWidget#Sidebar::item {{
        padding: 12px;
        border-radius: 6px;
        margin: 4px;
    }}
    QListWidget#Sidebar::item:selected {{
        background-color: {accent};
        color: {bg_panel};
        font-weight: bold;
    }}
    QListWidget#Sidebar::item:hover:!selected {{
        background-color: {bg_item};
        color: {text_main};
    }}

    /* Thumbnail Grid */
    QListWidget#ThumbnailGrid {{
        background-color: {bg_main};
        border: none;
        padding: 10px;
    }}
    QListWidget#ThumbnailGrid::item {{
        background-color: {bg_item};
        border: 2px solid transparent;
        border-radius: 8px;
        padding: 5px;
    }}
    QListWidget#ThumbnailGrid::item:selected {{
        border: 2px solid {accent};
        background-color: {bg_item_hover};
    }}
    
    /* Inputs */
    QLineEdit {{
        background-color: {bg_item};
        border: 1px solid {border_color};
        border-radius: 6px;
        padding: 8px;
        color: {text_main};
    }}
    QLineEdit:focus {{
        border: 1px solid {accent};
        background-color: {bg_main};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {bg_item_hover};
        color: {text_main};
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    QPushButton:hover {{ background-color: {bg_item}; }}
    QPushButton:pressed {{ background-color: {border_color}; }}
    QPushButton:disabled {{ background-color: {border_color}; color: {text_dim}; }}
    
    /* Primary Button (Gradient-like Mor) */
    QPushButton#PrimaryBtn {{
        background-color: {accent};
        color: {bg_panel};
    }}
    QPushButton#PrimaryBtn:hover {{ background-color: {accent_hover}; }}
    QPushButton#PrimaryBtn:pressed {{ background-color: {accent_pressed}; }}
    QPushButton#PrimaryBtn:disabled {{ background-color: {bg_item_hover}; color: {text_dim}; }}

    /* Danger Button */
    QPushButton#DangerBtn {{
        background-color: {danger};
        color: {bg_panel};
    }}
    QPushButton#DangerBtn:hover {{ background-color: {danger_hover}; }}

    /* Labels */
    QLabel {{ color: {text_main}; }}
    QLabel#HeaderLabel {{
        font-size: 18px;
        font-weight: bold;
        color: {accent};
        margin-bottom: 10px;
    }}
    QLabel#TitleLabel {{ font-size: 20px; font-weight: bold; color: {text_main}; }}
    
    QFormLayout {{ padding: 10px; }}
    """
