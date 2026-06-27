"""
互動式正弦與餘弦波形繪圖應用程式
使用 numpy 進行數值運算，matplotlib 進行繪圖與互動控制
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 設定中文字型（微軟正黑體適用於 Windows；macOS 可用 'Arial Unicode MS' 或 'Heiti TC'）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# 建立圖表與軸
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # 預留空間給滑桿

# X 軸範圍：0 到 4π
x = np.linspace(0, 4 * np.pi, 1000)

# 初始參數
A_init = 1.0
omega_init = 1.0
phi_init = 0.0

# 繪製初始波形
sin_line, = ax.plot(x, A_init * np.sin(omega_init * x + phi_init),
                    label='y = A·sin(ωx + φ)', linewidth=2, color='#1f77b4')
cos_line, = ax.plot(x, A_init * np.cos(omega_init * x + phi_init),
                    label='y = A·cos(ωx + φ)', linewidth=2, color='#ff7f0e')

# 設定圖表屬性
ax.set_title('正弦（sin）與餘弦（cos）波形互動繪圖', fontsize=14)
ax.set_xlabel('x（弧度）', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-5.5, 5.5)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=11)

# ===== 建立滑桿 =====

# 振幅滑桿
ax_amp = plt.axes([0.15, 0.12, 0.7, 0.03])
slider_amp = Slider(ax_amp, '振幅 A', 0.1, 5.0, valinit=A_init)

# 頻率滑桿
ax_freq = plt.axes([0.15, 0.07, 0.7, 0.03])
slider_freq = Slider(ax_freq, '頻率 ω', 0.1, 10.0, valinit=omega_init)

# 相位偏移滑桿
ax_phase = plt.axes([0.15, 0.02, 0.7, 0.03])
slider_phase = Slider(ax_phase, '相位 φ', 0, 2 * np.pi, valinit=phi_init)


def update(val):
    """滑桿觸發的更新函式：根據當前滑桿值重新計算並更新波形"""
    A = slider_amp.val
    omega = slider_freq.val
    phi = slider_phase.val

    sin_line.set_ydata(A * np.sin(omega * x + phi))
    cos_line.set_ydata(A * np.cos(omega * x + phi))

    # 根據振幅動態調整 Y 軸範圍
    ax.set_ylim(-A * 1.2, A * 1.2)

    fig.canvas.draw_idle()  # 觸發重繪


# 註冊更新事件
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

plt.show()
