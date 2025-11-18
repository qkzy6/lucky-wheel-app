# streamlit_app.py
# (版本 10 - "选择指示器"版)

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
        
        # 计算 JS 最终需要停止的位置
        # 注意这里我们不再需要 centering_offset，因为指示框会处理居中
        final_position = -(stop_index * item_height_px) 

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
                position: relative; /* 🔴 改动点 1 (A): 容器需要相对定位 */
            }}
            .reel {{ 
                position: absolute; /* 🔴 改动点 1 (B): 滚筒需要绝对定位 */
                width: 100%;
                top: 0;
                left: 0;
            }}
            .item {{
                height: {item_height_px}px; 
                line-height: {item_height_px}px;
                font-size: {font_size_px}px; 
                font-weight: bold; 
                text-align: center;
                box-sizing: border-box; 
                border: 1px solid #FFD700; /* 默认金色边框 */
                transition: color 0.3s ease, font-weight 0.3s ease, border 0.3s ease;
            }}
            .item.winner {{
                color: #D90000; /* 大红色 */
                font-weight: 900; /* 加粗 */
                border-width: 3px;
            }}
            
            /* 🔴 改动点 2: 
               定义"选择指示器"样式
            */
            .selector-indicator {{
                position: absolute; /* 绝对定位 */
                width: calc(100% - 4px); /* 100% 减去容器的2px*2边框 */
                
                /* 精确居中 */
                top: 50%; 
                transform: translateY(-50%); 
                
                height: {item_height_px}px; 
                border: 4px solid #FF4500; /* 醒目的橙红色边框 */
                border-radius: 5px;
                z-index: 10; /* 确保它在滚筒之上 */
                pointer-events: none; /* 不会影响鼠标事件 */
                box-sizing: border-box;
                box-shadow: 0 0 15px rgba(255, 69, 0, 0.7); /* 发光效果 */
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
            /* 🔴 改动点 3: 
               在滚筒之后添加选择指示器
            */
            <div class="selector-indicator"></div> 
        </div>

        <script>
        window.onload = function() {{
            const reel = document.getElementById('reel');
            if (!reel) {{ return; }} 

            const stopIndex = {stop_index};
            const finalPosition = {final_position};
            const itemHeight = {item_height_px}; // JS里也需要

            // (阶段 1: 立即开始无限循环)
            reel.style.animation = 'spin 0.5s linear infinite';

            // (阶段 2: 2.5秒后, 准备停止)
            setTimeout(() => {{
                const container = document.getElementById('slot-container');
                const containerRect = container.getBoundingClientRect();
                const reelRect = reel.getBoundingClientRect();
                
                // 计算滚筒在容器内的 Y 偏移量
                const currentY = reelRect.top - containerRect.top;

                reel.style.animation = 'none'; 
                reel.style.transition = 'none'; 
                reel.style.transform = `translateY(${{currentY}}px)`;
                reel.offsetHeight; 

                // 修正 finalPosition，使中奖项居中
                // (container_height / 2) - (itemHeight / 2) 是指示框中心到顶部的距离
                const correctedFinalPosition = finalPosition + (container_height / 2) - (itemHeight / 2);

                reel.style.transition = 'transform 3s ease-out'; // 3秒减速
                reel.style.transform = `translateY(${{correctedFinalPosition}}px)`;
            }}, 2500); 
            
            // (阶段 3: 5.5秒后, 高亮中奖项)
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
