# streamlit_app.py
# (版本 9 - "全金框"版)

import streamlit as st
import random
import streamlit.components.v1 as components
import time

def create_wheel_app():
    st.title("🎉 幸运大转盘 (网页版) 🎉")

    # ========== 配置 ==========
    items_config = [
        ("谢谢参与", 50),   
        ("10积分",   15),   
        ("20积分",   10),   
        ("50积分",   10),   
        ("100积分",   5),   
        ("神秘大奖",  3),   
    ]
    items_list = items_config * 5 
    labels = [item[0] for item in items_list]
    weights = [item[1] for item in items_list]
    n_items = len(items_list) 
    base_len = len(items_config) 

    # --- 视觉参数 ---
    item_height_px = 70  
    font_size_px = 30  
    visible_items = 3  
    container_height = item_height_px * visible_items 
    one_loop_height = base_len * item_height_px

    # --- Streamlit 交互 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):
        
        # --- (Python) 抽奖逻辑 ---
        chosen_base_index = random.choices(list(range(base_len)), weights=[w[1] for w in items_config], k=1)[0]
        result = items_config[chosen_base_index][0]
        
        stop_index = (base_len * 2) + chosen_base_index
        centering_offset = (item_height_px * (visible_items - 1) / 2)
        final_position = -((stop_index * item_height_px) - centering_offset)

        # --- HTML/CSS/JS ---
        reel_items_html = ""
        for label in labels:
            reel_items_html += f'<div class="item">{label}</div>'

        slot_machine_html = f"""
        <style>
            .slot-container {{
                width: 100%; height: {container_height}px;
                overflow: hidden; border: 2px solid #444; border-radius: 5px;
                background: #f9f9f9; box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
            }}
            .reel {{ 
                /* 默认无动画，JS会添加 */
            }}
            
            /* 🔴 改动点 1: 
               修改 .item 的默认边框
            */
            .item {{
                height: {item_height_px}px; 
                line-height: {item_height_px}px;
                font-size: {font_size_px}px; 
                font-weight: bold; 
                text-align: center;
                box-sizing: border-box; 
                
                /* 默认边框: 1px 金色实线 */
                border: 1px solid #FFD700; /* #FFD700 是金色的色号 */
                
                /* (移除) 原来的 "border-bottom: 1px dashed #ccc;" */
                
                /* 让边框和颜色变化更平滑 */
                transition: color 0.3s ease, font-weight 0.3s ease, border 0.3s ease;
            }}
            
            /* 🔴 改动点 2: 
               .winner 样式现在是"加粗"边框和"变红"字体
            */
            .item.winner {{
                color: #D90000; /* 大红色 */
                font-weight: 900; /* 加粗 */
                
                /* 边框从 1px 加粗到 3px */
                border-width: 3px;
            }}
            
            @keyframes spin {{
                0% {{ transform: translateY(0); }}
                100% {{ transform: translateY(-{one_loop_height}px); }}
            }}
        </style>

        <div class="slot-container" id="slot-container">
            <div class="reel" id="reel">
                {reel_items_html}
            </div>
        </div>

        <script>
        /* (JS 部分与 V8 完全相同，无需改动) */
        window.onload = function() {{
            const reel = document.getElementById('reel');
            if (!reel) {{ return; }} 

            const stopIndex = {stop_index};
            const finalPosition = {final_position};

            reel.style.animation = 'spin 0.5s linear infinite';

            setTimeout(() => {{
                const containerTop = reel.parentElement.getBoundingClientRect().top;
                const reelTop = reel.getBoundingClientRect().top;
                const currentY = reelTop - containerTop;

                reel.style.animation = 'none'; 
                reel.style.transition = 'none'; 
                reel.style.transform = `translateY(${{currentY}}px)`;
                reel.offsetHeight; 

                reel.style.transition = 'transform 3s ease-out'; 
                reel.style.transform = `translateY(${{finalPosition}}px)`;
            }}, 2500); 
            
            setTimeout(() => {{
                const allItems = document.querySelectorAll('.item');
                const winner = allItems[stopIndex];
                if (winner) {{
                    winner.classList.add('winner');
                }}
            }}, 5500); 

        }};
        </script>
        """

        # 4. (Streamlit) 渲染这个HTML组件
        components.html(slot_machine_html, height=container_height + 10) 
        
        # 5. (Streamlit) 在组件下方显示最终结果
        result_placeholder = st.empty()
        
        # 6. (Python) 等待动画播完 (2.5 + 3 = 5.5秒)
        time.sleep(5.5) 
        
        result_placeholder.success(f"恭喜！您抽中了： {result}")

        if "谢" not in result and "无" not in result:
            st.balloons()
            
    else:
        st.info("请点击上面的按钮开始抽奖")

# --- 程序入口 ---
if __name__ == "__main__":
    create_wheel_app()
