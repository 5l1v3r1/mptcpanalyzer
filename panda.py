#!/usr/bin/env python3
###########################################################
# author: Matthieu coudron , matthieu.coudron@lip6.fr
# this script requires wireshark (& gnuplot >4.6) to be installed
# http://stackoverflow.com/questions/11500469/plotting-columns-by-calling-their-header-with-gnuplot
# import csv
# TODO list
# -auto conversion from pcap to csv
# -reenable sql support (panda can read from SQL
# -ability to load filesfrom the interpreter
# -add color with ncurses (problematic with utf8 ?)
# -would like to draw a bar with the repartition of the data between the different subflows with sthg like
#  plot(kind='barh', stacked=True);
import sys
import argparse
import logging
import os
import readline
import glob
from mptcpanalyzer.tshark import TsharkExporter
import pandas as pd
import matplotlib.pyplot as plt
import shlex
import cmd
import traceback

tshark_bin = "/home/teto/wireshark/run/tshark"

log = logging.getLogger("mptcpanalyzer")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

# subparsers that need an mptcp_stream should inherit this parser
stream_parser = argparse.ArgumentParser(
    description='',
    # else conflicts with
    add_help=False
)

stream_parser.add_argument("mptcp_stream", action="store", type=int, help="identifier of the MPTCP stream")

# TODO ca le generer des scripts dans le dossier plot
# plot_types = {
#     'mappings_simple': "plots/mappings/mappings_per_subflow.plot",
#     'mappings_time': "plots/mappings/time_vs_mappings.plot",
#     # this one uses multiplot
#     'mappings_ack': "plots/mappings/mappings_and_ack.plot",
#     # 'mptcp_rtt': '',
# } 

# 
#  tshark -T fields -e _ws.col.Source -r /mnt/ntfs/pcaps/demo.pcap
# TODO merge these fields (always) when tshark exports ?
mandatory_fields = [
    'ipsrc',
    'ipdst',
    'sport',
    'dport',
    'mptcpstream',
    'tcpstream',
]

plot_types = ["dsn", "tcpseq", "dss"]

class MpTcpAnalyzer(cmd.Cmd):
    intro = """
        Welcome in mptcpanalyzer (http://github.com/teto/mptcpanalyzer)
        Press ? to get help
        """
    ruler = "="
    # ruler = "============================"
    prompt = ">"
    def __init__(self, pcap_file, input=None):
        #completekey='tab', stdin=None, stdout=None
        # stdin ?
        self.prompt = "%s >" % pcap_file 

        # if loading commands from a file, we disable prompt not to pollute output
        if input:
            self.use_rawinput = False
            self.prompt = ""
            self.intro = ""
        super().__init__(completekey='tab', stdin=input)
# , sep='|'
        self.data = pd.read_csv(pcap_file, sep='|')
        #print(self.data.col
        # list(self.data.columns)
        # TODO run some check on the pcap to check if column names match
        # 

    def do_ls(self, mptcpstream):
        """ list mptcp subflows 
                [mptcp.stream id]
        """
        print(mptcpstream)
        try:
            mptcpstream = int(mptcpstream)
        except ValueError as e:
            print("Expecting the mptcp.stream id as argument")
            return

        print('hello fpr mptcpstream %d' % mptcpstream)
        group = self.data[ self.data.mptcpstream == mptcpstream]
        tcpstreams = group.groupby('tcpstream')
        print("mptcp.stream %d has %d subflow(s): " % (mptcpstream, len(tcpstreams)))
        for tcpstream, gr2 in tcpstreams:
            # print(gr2)
            # print(group['ipsrc'])
            print("\ttcp.stream %d : %s:%d <-> %s:%d" % (
                tcpstream, gr2['ipsrc'].iloc[0], gr2['sport'].iloc[0], gr2['ipdst'].iloc[0], gr2['dport'].iloc[0])
                  )

    def complete_ls(self, args):
        """ help to complete the args """
        pass


    def do_summary(self, mptcpstream):
        """
        Summarize contributions of each subflow
                [mptcp.stream id]
        For now it is naive, does not look at retransmissions ?
                """
        print("arg=", mptcpstream)
        try:
            mptcpstream = int(mptcpstream)
        except ValueError as e:
            print("Expecting the mptcp.stream id as argument")
            return
 
        df = self.data[self.data.mptcpstream == mptcpstream]
        # for instance 
        dsn_min = df.dss_dsn.min()
        dsn_max = df.dss_dsn.max()
        total_transferred = dsn_max - dsn_min
        d = df.groupby('tcpstream')
        # drop_duplicates(subset='rownum', take_last=True)
        print("mptcpstream %d transferred %d" % (mptcpstream, total_transferred))
        for tcpstream, group in d:
            subflow_load = group.drop_duplicates(subset="dss_dsn").dss_length.sum()
            print(subflow_load)
            print(subflow_load)
            print('tcpstream %d transferred %d out of %d, hence is responsible for %f%%' %( tcpstream, subflow_load, total_transferred, subflow_load/total_transferred * 100 ))

    def do_lc(self, *args):
        """ List mptcp connections """
        print('mptcp connections')
        self.data.describe()
        mp = self.data.groupby("mptcpstream")
        for mptcpstream, group in mp:
            self.do_ls(mptcpstream)
            # print("mptcp.stream %d : %s <-> %s " % (mptcpstream, group['ip4src'][0], group['ip4dst'][0]))
        # print(mp['ip4src'])
        # le nunique s'applique sur une liste et permet d'avoir
        # mp.ip4src.nth(0)[0]


# def plot_tcp
    # def plot_mptcp
    # def do_pdsn(self, args):
    def do_p(self, args):
        """
        Alias for plot
        """
        self.plot(args)

    def do_plot(self, args):
        """
        Plot DSN vs time
            [mptcp.stream] 
        """
        self.plot_mptcpstream(args)

    def help_plot(self):
        print("Hello world")

    def complete_plot(self,args):
        pass

    def plot_mptcpstream(self, args):
        """
        global member used by others do_plot members *
        """

    # def do_plot_ack(self, args):
    # def do_plot_dss(self, args):
    # todo plot app_latency too

        parser = argparse.ArgumentParser(description='Generate MPTCP stats & plots')
        # parse
        parser.add_argument('field', action="store", choices=plot_types, help='Field to draw (see mptcp_fields.json)')
        parser.add_argument('mptcpstream', action="store", type=int, help='mptcp.stream id')
        parser.add_argument('out', action="store", nargs="?", default="output.png", help='Name of the output file')
        parser.add_argument('--display', action="store_true", help='will display the generated plot')
        # shlex.split(args) ?
        try:
            # args = parser.parse_args( shlex.split(field + ' ' + args))
            args = parser.parse_args( shlex.split(args))
        except SystemExit:
            return

        print(args)
        # returns a DataFrame
        dat = self.data[self.data.mptcpstream == args.mptcpstream]
        if not len(dat.index):
            print("no packet matching mptcp.stream %d" % args.mptcpstream)
            return
        
        # dssRawDSN could work as well
        # plot (subplots=True)
        fig = plt.figure()
        plt.title("hello world")
        # ax = tcpstreams[args.field].plot(ax=fig.gca())
        # want 
        # columns allows to choose the correct legend
        # df = self.data
        dat.set_index("reltime", inplace=True)
        tcpstreams = dat.groupby('tcpstream')
        # print(df)
        pplot = tcpstreams[args.field].plot(ax=fig.gca(),
            # x=tcpstreams["reltime"],
            # x="Relative time", # ne marche pas
            title="Data Sequence Numbers over subflows", 
            # use_index=False,
            # legend=True,
            lw=3
            )
        ax = fig.gca()
        # print(dir(pplot))
        # pplot.ax
        ax.set_xlabel("Relative time")
        # pplot.set_xlabel("Time")
        # ax.set_ylabel("DSN")
        # fig = ax.get_figure()
        # for axes in plot:
            # print("Axis ", axes)
            # fig = axes.get_figure()
            # fig.savefig("/home/teto/test.png")
        # fig = plot.get_figure()
        args.out = os.path.join(os.getcwd(), args.out)
        fig.savefig(args.out)
        # os.path.realpath
        # lines, labels = ax1.get_legend_handles_labels()
        cmd="xdg-open %s" % (args.out,) 
        print (cmd) 
        if args.display:
            os.system(cmd)


    def do_q(self,*args):
        """
        Quit/exit program
        """
        return True

    def do_EOF(self, line):
        """
        """
        return True

    def preloop(intro):
        print(intro)

def main():
    parser = argparse.ArgumentParser(
        description='Generate MPTCP stats & plots'
    )
    parser.add_argument("input", action="store", help="Input file that will be converted in csv if needed")
    parser.add_argument("--regen", "-r", action="store_true", help="Force the regen")
    parser.add_argument("--batch", "-b", action="store", type=str, help="Accepts a filename as argument from which commands will be loaded")
    # parser.add_argument("--command", "-c", action="store", type=str, nargs="*", help="Accepts a filename as argument from which commands will be loaded")


    # TODO here one could use parse_known_args
    args, unknown_args = parser.parse_known_args(sys.argv[1:])

    basename, ext = os.path.splitext(os.path.basename(args.input))
    csv_filename = basename + ".csv"
   
    if not ext == ".csv":
        print("%s format is not supported as is. Needs to be converted first" % (args.input))
        
        cache = os.path.isfile(csv_filename) 
        if cache:
            print("A cache %s was found" % csv_filename)
        # if matching csv does not exist yet or if generation forced
        if not cache or args.regen:
            log.info("Preparing to convert %s into %s" % (args.input, csv_filename))
            exporter = TsharkExporter(tshark_bin)
            retcode, stderr = exporter.export_to_csv(args.input, csv_filename)
            print("exporter exited with code=", retcode)
            if retcode:
                raise Exception(stderr)
    
    log.info(" %s " % (args.input))
  
    # if I load from 
    input = None
    try:
        if args.batch:
            input = open(args.batch, 'rt')
        # stdin=input
        # Disable rawinput module use
        # use_rawinput = False
        

        # here I want to generate automatically the csv file 
        analyzer = MpTcpAnalyzer(csv_filename, input)

        # if extra parameters passed via the cmd line, consider it is
        if not input and unknown_args:
            analyzer.onecmd( ' '.join(unknown_args))
        else:
            analyzer.cmdloop() 
    except Exception as e:
        print("An error happened %s " % e) 
        print(traceback.print_exc())
    finally:

        input.close() if input else None


if __name__ == '__main__':
    main()

#  vim: set et fenc=utf-8 ff=unix sts=4 sw=4 ts=4 : 
