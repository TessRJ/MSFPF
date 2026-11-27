"""Proyecto Final: Sistema Endocrino "Enfermedad de Hashimoto"

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno, Número de control y Correo institucional: 
                   Castañeda Nieblas Lorena Lizel   /  23210695 /  L23210695@tijuana.tecnm.mx
                   Preciado Amezquita Carlos Samuel / C19211840 / LC19211840@tijuana.tecnm.mx
                   Rincon Jumenez Tessa             /  22210795 /  L22210795@tijuana.tecnm.mx
                   Vazquez Alvear Nicole            / C20210923 / LC20210923@tijuana.tecnm.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""


import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

t = np.linspace(0.0, 2.0, 2001)
u = np.ones_like(t)  # Voltaje de entrada escalón de 1 V

# 1. Sistema Control en lazo abierto
num_ctrl = [0.8]
den_ctrl = [0.015, 1.0]
sys_ctrl = signal.TransferFunction(num_ctrl, den_ctrl)
_, y_ctrl, _ = signal.lsim(sys_ctrl, U=u, T=t)

# 2. Sistema Caso en lazo abierto
num_caso = [0.18]
den_caso = [0.08, 1.0]
sys_caso = signal.TransferFunction(num_caso, den_caso)
_, y_caso, _ = signal.lsim(sys_caso, U=u, T=t)

# 3. Controlador PIDN aplicado sobre el Caso
P = 2000
I = 33480
D = 0.1112
N = 20000

num_pid = np.array([P + D * N, P * N + I, I * N], dtype=float)
den_pid = np.array([1.0, N, 0.0], dtype=float)

# Lazo abierto L(s) = G_pid(s) * G_caso(s)
num_ol = np.convolve(num_pid, np.array(num_caso, dtype=float))
den_ol = np.convolve(den_pid, np.array(den_caso, dtype=float))

# Lazo cerrado T(s) = L(s) / (1 + L(s)) siguiendo la curva de Control
max_len = max(len(num_ol), len(den_ol))
num_ol_pad = np.pad(num_ol, (max_len - len(num_ol), 0))
den_ol_pad = np.pad(den_ol, (max_len - len(den_ol), 0))

sys_pid_caso = signal.TransferFunction(num_ol_pad, den_ol_pad + num_ol_pad)
_, y_pid_caso, _ = signal.lsim(sys_pid_caso, U=y_ctrl, T=t)

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.edgecolor"] = "#444444"
plt.rcParams["axes.linewidth"] = 0.8

fig, ax = plt.subplots(figsize=(15, 7.2), dpi=150)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.set_xlim(0.0, 2.0)
ax.set_ylim(-0.1, 1.1)
ax.set_xticks(np.arange(0.0, 2.01, 0.2))
ax.set_yticks(np.arange(-0.1, 1.11, 0.1))

ax.set_xticklabels(["0", "0.2", "0.4", "0.6", "0.8", "1", "1.2", "1.4", "1.6", "1.8", "2"], fontsize=8)
ax.set_yticklabels(["-0.1", "0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1", "1.1"], fontsize=8)

ax.grid(True, which="major", linestyle="-", linewidth=0.55, color="#888888", alpha=0.85)
ax.tick_params(axis="both", which="major", direction="in", top=True, right=True, length=5, width=0.7, color="#333333")

ax.plot(t, u,          color="#228B22", linestyle="-", linewidth=1.4, zorder=1, label="Ve(t)")
ax.plot(t, y_caso,     color="#0000FF", linestyle="-", linewidth=1.4, zorder=2, label="Vs(t): Caso")
ax.plot(t, y_ctrl,     color="#00FFFF", linestyle="-", linewidth=3.0, zorder=4, label="Vs (t): Control")
ax.plot(t, y_pid_caso, color="#8B4513", linestyle="-.",  linewidth=1.5, zorder=10, label="PID(t)")

legend = ax.legend(
    loc="lower right",
    frameon=True,
    facecolor="white",
    edgecolor="#333333",
    fontsize=8.2,
    borderpad=0.35,
    labelspacing=0.28,
)
legend.get_frame().set_linewidth(0.8)

plt.tight_layout()
plt.savefig("Respuesta del sistema.pdf")
plt.show()