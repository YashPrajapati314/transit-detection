import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

# Create a PDF file to store the plots
with PdfPages('') as pdf:
    # Set up a figure with subplots (2 rows, 2 columns in this example)
    fig, axs = plt.subplots(2, 2, figsize=(8.5, 11))  # Letter size page

    x = np.linspace(0, 10, 100)

    # First plot
    axs[0, 0].plot(x, np.sin(x))
    axs[0, 0].set_title('Sine')

    # Second plot
    axs[0, 1].plot(x, np.cos(x))
    axs[0, 1].set_title('Cosine')

    # Third plot
    axs[1, 0].plot(x, np.tan(x))
    axs[1, 0].set_title('Tangent')

    # Fourth plot
    axs[1, 1].plot(x, np.exp(-x))
    axs[1, 1].set_title('Exponential Decay')

    # Adjust layout and save the figure to the PDF
    plt.tight_layout()
    pdf.savefig(fig)  # Save the whole figure on a single PDF page
    plt.close(fig)
