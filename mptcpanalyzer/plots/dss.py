import mptcpanalyzer.plot as plot
import mptcpanalyzer as mp
import matplotlib.pyplot as plt
import matplotlib as mpl
from itertools import cycle
import logging
from mptcpanalyzer.parser import gen_pcap_parser
from mptcpanalyzer.debug import debug_dataframe

log = logging.getLogger(__name__)

class DssLengthHistogram(plot.Matplotlib):
    """
    Plots histogram

    .. warning:: WIP
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            args,
            title="DSS Length",
            **kwargs
        )

    def default_parser(self, *args, **kwargs):

        pcaps = {
            "pcap": plot.PreprocessingActions.Preload | plot.PreprocessingActions.FilterStream,
        }

        parser = gen_pcap_parser(pcaps, direction=True)
        # force to choose a destination
        parser.add_argument('--dack', action="store_true", default=False,
            help="Adds data acks to the graph")

        # can only be raw as there are no relative dss_dsn exported yet ?
        # parser.add_argument('--relative', action="store_true", default=False,
        #         help="Adds data acks to the graph")
        parser.description = "TEST description"
        parser.epilog = "test epilog"
        return parser

    def plot(self, df, mptcpstream, **kwargs):

        fig = plt.figure()
        axes = fig.gca()
        df.set_index("reltime", inplace=True)
        field = "dss_length"
        pplot = df[field].plot.hist(
            ax=axes,
            legend=True,
            grid=True,
        )
        return fig


class DSSOverTime(plot.Matplotlib):
    """
    Draw small arrows with dsn as origin, and a *dss_length* length etc...
    Also allow to optionally display dataack

    As the generated plot can end up being quite rich, it is a good idea to specify
    a |matplotlibrc| with high dimensions and high dpi.

    Todo:
        - if there is an ack add that to legend
        - ability to display relative #seq
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            title="dsn",
            x_label="Time (s)",
            y_label="Data Sequence Number",
            **kwargs
        )

    def default_parser(self, *args, **kwargs):

        pcaps = {
            "pcap": plot.PreprocessingActions.Preload | plot.PreprocessingActions.FilterStream,
        }

        parser = gen_pcap_parser(pcaps, direction=True)

        # force to choose a destination
        parser.add_argument('--dack', action="store_true", default=False,
            help="Adds data acks to the graph")

        # can only be raw as there are no relative dss_dsn exported yet ?
        # parser.add_argument('--relative', action="store_true", default=False,
        #         help="Adds data acks to the graph")
        parser.description = "TEST description"
        parser.epilog = "test epilog"
        return parser

    def plot(self, pcap, destination=None, dack=False, relative=None, **args):
        """
        Might be

        """
        dack_str = "dss_rawack"
        dsn_str = "dss_dsn"

        ymin, ymax = float('inf'), 0

        debug_dataframe(pcap, "dss")

        rawdf = pcap.set_index("reltime")
        con = rawdf.mptcp.connection(streamid)
        df = con.fill_dest(df)

        # only select entries with a dss_dsn
        # df_forward = self.preprocess(rawdf, destination=destination, extra_query="dss_dsn > 0", **args)
        print(destination)
        # print(destinations)
        # tcpdest or mptcpdest
        df_forward = pcap[pcap.mptcpdest == destination]
        df_forward = df_forward[df_forward.dss_dsn > 0]
        print(df_forward)

        # compute limits of the plot
        ymin, ymax = min(ymin, df_forward[dsn_str].min()), max(ymax, df_forward[dsn_str].max())
        print("setting ymin/ymax", ymin, ymax)

        fig = plt.figure()
        axes = fig.gca()

        def show_dss(idx, row, style):
            """
            dss_dsn
            """
            # returns a FancyArrow
            res = axes.arrow(idx, int(row[dsn_str]), 0, row["dss_length"],
                head_width=0.05, head_length=0.1, **style)
            res.set_label("hello")
            return res

        handles, labels = axes.get_legend_handles_labels()


        # TODO cycle manually through
        cycler = mpl.rcParams['axes.prop_cycle']
        styles = cycle(cycler)
        legends = []
        legend_artists = []

        ### Plot dss dsn (forward)
        ######################################################
        for tcpstream, df in df_forward.groupby('tcpstream'):
            style = next(styles)
            print("arrows for tcpstream %d", tcpstream)

            style = next(styles)

            artist_recorded = False
            # TODO itertuples should be faster
            for index, row in df_forward.iterrows():
                artist = show_dss(index, row, style)
                if not artist_recorded:
                    legend_artists.append(artist)
                    artist_recorded = True

            if artist_recorded:
                legends.append("dss for Subflow %d" % tcpstream)


        ### if enabled, plot dack (backward)
        ######################################################
        if dack:
            df_backward = self.preprocess(rawdf, **args, destination=mp.reverse_destination(destination),
                    extra_query=dack_str + " >=0 ")

            for tcpstream, df in df_backward.groupby('tcpstream'):
                # marker = next(markers)
                if df.empty:
                    log.debug("No dack for tcpstream %d" % tcpstream)
                else:
                    ax1 = df[dack_str].plot.line(ax=axes, legend=False)
                    lines, labels = ax1.get_legend_handles_labels()
                    legend_artists.append(lines[-1])
                    legends.append("dack for sf %d" % tcpstream)

        # location: 3 => bottom left, 4 => bottom right
        axes.legend(legend_artists, legends, loc=4)
        axes.set_ylim([ymin, ymax])

        return fig
