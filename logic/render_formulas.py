from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import io

def render_formula(X='x', Y='y', H='h', K='k', A='a', B='b'):
    plt.clf()
    fig = plt.figure(figsize=(6, 2), dpi=100)
    plt.axis('off')

    formula = rf"\frac{{({X} - {H})^2}}{{{A}^2}} + \frac{{({Y} - {K})^2}}{{{B}^2}} = 1"
    plt.text(0.5, 0.5, f"${formula}$", fontsize=20, ha='center', va='center')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    plt.close(fig)
    img = Image.open(buf)
    return ImageTk.PhotoImage(img)
    
def render_formula_general(formula_latex):
    plt.clf()
    fig = plt.figure(figsize=(6, 1.5), dpi=100)
    plt.axis('off')
    plt.text(0.5, 0.5, f"${formula_latex}$", fontsize=16, ha='center', va='center')
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    buf.seek(0)
    plt.close(fig)
    img = Image.open(buf)
    return ImageTk.PhotoImage(img)