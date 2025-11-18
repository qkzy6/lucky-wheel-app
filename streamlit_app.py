# streamlit_app.py
# (版本 12 - 神秘大奖动画版)

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
    
    # --- 图片 URL (重要!) ---
    # 请确保这张图片在 GitHub 仓库的根目录，或者提供一个有效的公共网络链接
    # 如果图片在 GitHub 根目录，路径就是 'image.png' (或者您图片的文件名)
    mysterious_image_url = "https://i.imgur.com/your-image-id.png" # 🔴 请替换为您的图片链接

    # --- Streamlit 交互 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):
        
        # --- (Python) 抽奖逻辑 ---
        chosen_base_index = random.choices(list(range(base_len)), weights=[w[1] for w in items_config], k=1)[0]
        result = items_config[chosen_base_index][0]
        
        stop_index = (base_len * 2) + chosen_base_index
        final_position_top_aligned = -(stop_index * item_height_px) 

        # --- HTML/CSS/JS ---
        reel_items_html = ""
        for label in labels:
            reel_items_html += f'<div class="item">{label}</div>'

        # 🔴 新增: 神秘大奖图片容器
        mystery_image_html = ""
        if result == "神秘大奖":
            mystery_image_html = f"""
            <div id="mystery-image-container" class="mystery-image-container">
                <img src="{mysterious_image_url}" alt="神秘大奖" class="mystery-image">
            </div>
            """

        slot_machine_html = f"""
        <style>
            .slot-container {{
                width: 100%; height: {container_height}px;
                overflow: hidden; border: 2px solid #444; border-radius: 5px;
                background: #f9f9f9; box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
                position: relative; 
            }}
            .reel {{ 
                position: absolute; width: 100%; top: 0; left: 0;
            }}
            .item {{
                height: {item_height_px}px; 
                line-height: {item_height_px}px;
                font-size: {font_size_px}px; 
                font-weight: bold; 
                text-align: center;
                box-sizing: border-box; 
                border: 1px solid transparent; border-bottom: 1px dashed #ccc;
                transition: color 0.3s ease, font-weight 0.3s ease, border 0.3s ease;
            }}
            .item.winner {{
                color: #D90000; font-weight: 900; border: 3px solid #FF4500;
            }}
            .selector-indicator {{
                position: absolute; width: calc(100% - 4px); 
                top: 50%; transform: translateY(-50%); 
                height: {item_height_px}px; 
                border: 4px solid #FF4500; border-radius: 5px;
                z-index: 10; pointer-events: none; box-sizing: border-box;
                box-shadow: 0 0 15px rgba(255, 69, 0, 0.7); 
            }}
            
            @keyframes spin {{
                0% {{ transform: translateY(0); }}
                100% {{ transform: translateY(-{one_loop_height}px); }}
            }}

            /* 🔴 新增 CSS: 神秘大奖图片动画 */
            .mystery-image-container {{
                position: fixed; /* 固定在视口 */
                top: -100vh; /* 初始位置: 完全在屏幕上方 */
                left: 0;
                width: 100vw; /* 宽度填满屏幕 */
                height: 100vh; /* 高度填满屏幕 */
                display: flex; /* 弹性布局居中图片 */
                justify-content: center;
                align-items: center;
                background: rgba(0,0,0,0.8); /* 半透明黑色背景 */
                z-index: 1000; /* 确保在最顶层 */
                opacity: 0; /* 初始透明度为0 */
                visibility: hidden; /* 初始不可见 */
                transition: opacity 0.5s ease-in-out; /* 透明度渐变 */
            }}
            .mystery-image-container.active {{
                animation: slide-in-out 8s forwards; /* 8秒动画 */
                opacity: 1;
                visibility: visible;
            }}
            .mystery-image {{
                max-width: 90%; /* 图片最大宽度 */
                max-height: 90%; /* 图片最大高度 */
                object-fit: contain; /* 保持图片比例 */
                border: 5px solid gold; /* 金色边框 */
                box-shadow: 0 0 50px rgba(255,215,0,0.8); /* 金色发光 */
            }}

            @keyframes slide-in-out {{
                0% {{ top: -100vh; opacity: 0; }} /* 开始: 完全在上方, 透明 */
                10% {{ top: 0vh; opacity: 1; }} /* 1秒内出现, 下滑到顶部 */
                60% {{ top: 0vh; opacity: 1; }} /* 停留5秒 */
                70% {{ top: -100vh; opacity: 0; }} /* 1秒内消失, 上滑 */
                100% {{ top: -100vh; opacity: 0; visibility: hidden; }} /* 结束: 完全消失 */
            }}

        </style>

        <div class="slot-container" id="slot-container">
            <div class="reel" id="reel">
                {reel_items_html}
            </div>
            <div class="selector-indicator"></div> 
        </div>
        
        {mystery_image_html} /* 🔴 新增: 将图片 HTML 放在这里 */

        <script>
        window.onload = function() {{
            const reel = document.getElementById('reel');
            if (!reel) {{ return; }} 

            const stopIndex = {stop_index};
            const itemHeight = {item_height_px};
            const containerHeight = {container_height}; 
            const finalPositionTopAligned = {final_position_top_aligned};

            reel.style.animation = 'spin 0.5s linear infinite';

            setTimeout(() => {{
                const container = document.getElementById('slot-container');
                const containerRect = container.getBoundingClientRect();
                const reelRect = reel.getBoundingClientRect();
                const currentY = reelRect.top - containerRect.top;

                reel.style.animation = 'none'; 
                reel.style.transition = 'none'; 
                reel.style.transform = `translateY(${{currentY}}px)`;
                reel.offsetHeight; 

                const centeringOffset = (containerHeight / 2) - (itemHeight / 2);
                const finalPositionCentered = finalPositionTopAligned + centeringOffset;
                
                reel.style.transition = 'transform 3s ease-out'; 
                reel.style.transform = `translateY(${{finalPositionCentered}}px)`;
            }}, 2500); 
            
            setTimeout(() => {{
                const allItems = document.querySelectorAll('.item');
                const winner = allItems[stopIndex];
                if (winner) {{
                    winner.classList.add('winner');
                }

                // 🔴 新增: 如果是神秘大奖, 触发图片动画
                if ("{result}" === "神秘大奖") {{
                    const mysteryImageContainer = document.getElementById('mystery-image-container');
                    if (mysteryImageContainer) {{
                        mysteryImageContainer.classList.add('active'); // 激活动画
                    }}
                }}

            }}, 5500); // 滚筒停止并高亮
            
            // 🔴 新增: 图片动画总时长大约 8 秒，所以最终结果文字要延迟显示
            // 滚筒停止 (5.5s) + 图片动画 (8s) = 13.5s
            // Python的 sleep 必须与这个总时长匹配
        }};
        </script>
        """

        # 4. (Streamlit) 渲染这个HTML组件
        components.html(slot_machine_html, height=container_height + 10) 
        
        # 5. (Streamlit) 在组件下方显示最终结果
        result_placeholder = st.empty()
        
        # 6. (Python) 等待所有动画播完 (滚筒 5.5s + 图片 8s = 13.5s)
        time.sleep(13.5) # 🔴 调整总等待时间
        
        result_placeholder.success(f"恭喜！您抽中了： {result}")

        if "谢" not in result and "无" not in result:
            st.balloons()
            
    else:
        st.info("请点击上面的按钮开始抽奖")

# --- 程序入口 ---
if __name__ == "__main__":
    create_wheel_app()
