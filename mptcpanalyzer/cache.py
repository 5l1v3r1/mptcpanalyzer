import os
from typing import List, Tuple
import logging


log = logging.getLogger("mptcpanalyzer")


class Cache:
    """
    """

    def __init__(self, folder, disabled=False):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)
        self.disabled = disabled


    # self.csv_cachename)
    # , translator=str)
    # translator: converts filename to a specific
    def is_cache_valid(self, filename, depends: List[str]) -> Tuple[bool, str]:
        """
        Args:
            depends: List of files to check
        """
        log.debug("Checking cache for %s" % filename)
        is_cache_valid = False

        # todo rename to encode rather
        # cachename = self.matching_cache_filename(filename)

        # encode path to cache
        chunks = os.path.realpath(filename).split(os.path.sep)
        cachename = os.path.join(self.folder, '%'.join(chunks))

        if self.disabled:
            log.debug("Cache disabled, hence requested cache deemed invalid")
        elif os.path.isfile(cachename):
            log.info("A cache %s was found" % cachename)
            ctime_cached = os.path.getctime(cachename)
            # ctime_pcap = os.path.getctime(filename)
            # print(ctime_cached , " vs ", ctime_pcap)
            is_cache_valid = True
            for dependancy in depends:
                ctime_dep = os.path.getctime(dependancy)

                if ctime_cached > ctime_dep:
                    log.debug("Cache seems valid")
                else:
                    log.debug("Cache outdated by dependancy %s" % dependancy)
                    is_cache_valid = False
                    break
        else:
            log.debug("No cache %s found" % cachename)
        return is_cache_valid, cachename

    # def csv_cachename(self, filename):
    #     """
    #     Expects a realpath else
    #     """
    #     # create a list of path elements
    #     # from the absolute filename
    #     l = os.path.realpath(filename).split(os.path.sep)
    #     res = os.path.join(self.folder, '%'.join(l))
    #     # _, ext = os.path.splitext(filename)
    #     # if ext != ".csv":
    #     #     res += ".csv"
    #     return res


    def clean(self):
        print("Cleaning cache [%s]" % self.folder)
        for cached_csv in os.scandir(self.folder):
            log.info("Removing " + cached_csv.path)
            os.unlink(cached_csv.path)