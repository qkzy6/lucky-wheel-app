# streamlit_app.py
# (版本 3 - 修复了 f-string 和 JS 冲突)

import streamlit as st
import random
import streamlit.components.v1 as components
import time # (您在上一版代码中可能漏掉了这个导入)

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

    # --- Streamlit 交互 ---
    if st.button("开始抽奖!", type="primary", use_container_width=True):
        
        base_len = len(items_config)
        chosen_base_index = random.choices(list(range(base_len)), weights=[w[1] for w in items_config], k=1)[0]
        result = items_config[chosen_base_index][0]
        stop_index = (base_len * 2) + chosen_base_index
        item_height_px = 50 

        # --- HTML/CSS/JS ---
        reel_items_html = ""
        for label in labels:
            reel_items_html += f'<div class="item">{label}</div>'

        slot_machine_html = f"""
        <style>
            .slot-container {{
                width: 100%; height: {item_height_px}px;
                overflow: hidden; border: 2px solid #444; border-radius: 5px;
                background: #f9f9f9; box-shadow: inset 0 0 10px rgba(0,0,0,0.1);
            }}
            .reel {{ transition: none; transform: translateY(0); }}
            .item {{
                height: {item_height_px}px; line-height: {item_height_px}px;
                font-size: 20px; font-weight: bold; text-align: center;
                border-bottom: 1px dashed #ccc;
            }}
        </style>

        <div class="slot-container" id="slot-container">
            <div class="reel" id="reel">
                {reel_items_html}
            </div>
        </div>

        <script>
        (function() {{
            const reel = document.getElementById('reel');
            const stopIndex = {stop_index};
            const itemHeight = {item_height_px};

            const styleSheet = document.createElement("style");
            const randomSpin = -(Math.random() * 10000 + 10000); // JS 变量
            
            styleSheet.innerHTML = `
                @keyframes spin-fast {{
                    0% {{ transform: translateY(0); }}
                    
                    /* 🔴 修复点 1：使用 ${{...}} 来转义 */
                    100% {{ transform: translateY(${{randomSpin}}px); }} 
                }}
            `;
            document.head.appendChild(styleSheet);
            reel.style.animation = 'spin-fast 1.5s linear infinite';

            setTimeout(() => {{
                reel.style.animation = 'none'; 
                const finalPosition = -(stopIndex * itemHeight); // JS 变量
                
                reel.style.transition = 'transform 3s ease-out';
                
                /* 🔴 修复点 2：使用 ${{...}} 来转义 */
                reel.style.transform = `translateY(${{finalPosition}}px)`;
                
            }}, 2500); 
        }})();
        </script>
        """

        # 4. (Streamlit) 渲染这个HTML组件
        components.html(slot_machine_html, height=item_height_px + 10)
        
        # 5. (Streamlit) 在组件下方显示最终结果
        result_placeholder = st.empty()
        
        # 6. 等待动画播完再显示文字
        time.sleep(5.5) 
        
        result_placeholder.success(f"恭喜！您抽中了： {result}")

        if "谢" not in result and "无" not in result:
            st.balloons()
            
    else:
        st.info("请点击上面的按钮开始抽奖")

# --- 程序入口 ---
if __name__ == "__main__":
    create_wheel_app()
