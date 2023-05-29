import argparse
import time
import logging
import random

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations

'''
TO run on Cyton:
    python real_time_plot.py --board-id 0 --serial-port COM3
To run Synthetically:
    python real_time_plot.py
'''
class Graph:
    def __init__(self, board_shim):
        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate

        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title='FFT Plot',size=(800, 600))

        self._init_pens()

        # self._init_timeseries()
        self._init_fft()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()


    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.win.addPlot(row=i,col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            if i == 0:
                p.setTitle('TimeSeries Plot')
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)

    def _init_pens(self):
            self.pens = list()
            self.brushes = list()
            colors = ['#A54E4E', '#A473B6', '#5B45A4', '#2079D2', '#32B798', '#2FA537', '#9DA52F', '#A57E2F', '#A53B2F']
            for i in range(len(colors)):
                pen = pg.mkPen({'color': colors[i], 'width': 2})
                self.pens.append(pen)
                brush = pg.mkBrush(colors[i])
                self.brushes.append(brush)

    def _init_fft(self):
        self.fft_plot = self.win.addPlot(row=0, col=0)
        self.fft_plot.setTitle('FFT Plot')
        self.fft_plot.setLogMode(False, True)

        self.fft_curves = list()
        self.fft_size = DataFilter.get_nearest_power_of_two(self.sampling_rate)
        for i in range(len(self.exg_channels)):
            fft_curve = self.fft_plot.plot(pen=self.pens[i % len(self.pens)])
            # fft_curve.setDownsampling(auto=True, method='mean', ds=3)
            self.fft_curves.append(fft_curve)

    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)
        for count, channel in enumerate(self.exg_channels):
            # plot fft
            if data.shape[1] > self.fft_size:
                fft_data = DataFilter.perform_fft(data[channel], WindowFunctions.NO_WINDOW.value)
                lim = min(70, len(fft_data[0]))
                self.fft_curves[count].setData(abs(fft_data[1][0:lim]).tolist(), abs(fft_data[0][0:lim]).tolist())

        self.app.processEvents()


def main():
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=False, default=BoardIds.SYNTHETIC_BOARD)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.serial_port = args.serial_port
    params.timeout = args.timeout
    params.file = args.file
    try:
        board_shim = BoardShim(args.board_id, params)

        board_shim.prepare_session()
        board_shim.start_stream(450000, args.streamer_params)
        g = Graph(board_shim)

    except BaseException as e:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board_shim.is_prepared():
            logging.info('Releasing session')
            board_shim.release_session()


if __name__ == '__main__':
    main()