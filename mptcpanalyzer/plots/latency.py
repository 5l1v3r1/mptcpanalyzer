#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mptcpanalyzer.plot as plot
import panda as pd
import matplotlib.pyplot as plt
import os


# TODO provide several versions; one with histograms for instance
class DsnVsLatency(plot.Plot):

    def __init__(self):
        # super(self, "dsn")
        pass

    # def plot(self, data, *args, **kwargs):
    def plot(self, data, args): # *args, **kwargs):
        print("data=", data) 
        print("args", args)
        # parser = plot.Plot.default_parser()
        # args = parser.parse_args(*args)
        dat = data[data.mptcpstream == args.mptcpstream]
        if not len(dat.index):
            print("no packet matching mptcp.stream %d" % args.mptcpstream)
            return

        # dssRawDSN could work as well
        # plot (subplots=True)
        fig = plt.figure()
        # plt.title("hello world")
        # ax = tcpstreams[args.field].plot(ax=fig.gca())
        # want 
        # columns allows to choose the correct legend
        # df = self.data
        dat.set_index("reltime", inplace=True)
        tcpstreams = dat.groupby('tcpstream')
        # print(df)
        field = "dsn"
        pplot = tcpstreams[field].plot.line(
            # gca = get current axis
            ax=fig.gca(),
            # x=tcpstreams["reltime"],
            # x="Relative time", # ne marche pas
            title="Data Sequence Numbers over subflows", 
            # use_index=False,
            legend=True,
            # style="-o",
            grid=True,
            # xticks=tcpstreams["reltime"],
            # rotation for ticks
            # rot=45, 
            # lw=3
        )   
        # patches1, labels1 = ax1.get_legend_handles_labels()
        # ax.legend()
        # print(dir(pplot))
        # ax = pplot.axes[0].get_figure()
        ax = fig.gca()
        # print(dir(pplot))
        # pplot.ax
        # fig.set_xlabel("Relative time")
        # pplot.set_xlabel("Time")
        # ax.set_ylabel("DSN")
        # fig = ax.get_figure()
        # for axes in plot:
        # print("Axis ", axes)
        # fig = axes.get_figure()
        # fig.savefig("/home/teto/test.png")
        # fig = plot.get_figure()
        args.out = os.path.join(os.getcwd(), args.out)
        print("Saving into %s" % (args.out))
        fig.savefig(args.out)
        return True


# TODO provide several versions; one with histograms for instance
class LatencyHistogram(plot.Plot):

    def __init__(self):
        # super(self, "dsn")
        pass

    # def plot(self, data, *args, **kwargs):
    def plot(self, data, args):
        # print("data=", data) 
        print("args", args)
        # parser = plot.Plot.default_parser()
        # args = parser.parse_args(*args)
        dat = data[data.mptcpstream == args.mptcpstream]
        if not len(dat.index):
            print("no packet matching mptcp.stream %d" % args.mptcpstream)
            return

        # dssRawDSN could work as well
        # plot (subplots=True)
        # fig = plt.figure()
        # plt.title("hello world")
        # ax = tcpstreams[args.field].plot(ax=fig.gca())
        # want 
        # columns allows to choose the correct legend
        # df = self.data
        # dat.set_index("reltime", inplace=True)
        ax = dat.plot.hist(
            # gca = get current axis
            # ax=fig.gca(),
            by="latency",
            # x=tcpstreams["reltime"],
            # x="Relative time", # ne marche pas
            # title="Data Sequence Numbers over subflows", 
            # use_index=False,
            legend=False,
            # style="-o",
            grid=True,
            bins=10,
            # xticks=tcpstreams["reltime"],
            # rotation for ticks
            # rot=45, 
            # lw=3
        )   
        # patches1, labels1 = ax1.get_legend_handles_labels()
        # ax.legend()
        # print(dir(pplot))
        # ax = pplot.axes[0].get_figure()
        # ax = fig.gca()
        # print(dir(pplot))
        # pplot.ax
        ax.set_xlabel("Relative time")
        # ax.set_xlabel("Time")
        ax.set_ylabel("Latency")
        # fig = ax.get_figure()
        # for axes in plot:
        # print("Axis ", axes)
        fig = ax.get_figure()
        # fig.savefig("/home/teto/test.png")
        # fig = plot.get_figure()
        args.out = os.path.join(os.getcwd(), args.out)
        print("Saving into %s" % (args.out))
        fig.savefig(args.out)
        return True
