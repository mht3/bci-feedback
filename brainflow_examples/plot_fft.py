from matplotlib import pyplot as plt

'''
Plots FFT OpenBCI data processed by the brainflow library

Will have 8 channels for cyton and 16 for synthetic

fft_data: 2-dimensional array of fft_data for each channel.
'''
def plot_fft_data(fft_data):
        for channel, data in enumerate(fft_data):
            # Nyquist Shannon Sampling Theorem
            # Aliasing (overlap of repeated transforms) occurs at above X/2 the original sampling of rate about 120 Hz) 
            # So let's stop at 60 Hz
            data = abs(fft_data[channel][:60])
            # print(data)
            plt.plot(data)

        # plt.yscale("log")
        plt.ylabel("Amplitude (V)")
        plt.xlabel("Frequency (Hz)")
        plt.title("FFT Plot")
        plt.show()