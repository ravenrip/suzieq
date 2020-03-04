import time

from nubia import command, argument

from suzieq.cli.sqcmds.command import SqCommand
from suzieq.sqobjects.vlan import VlanObj


@command('vlan', help="Act on vlan data")
class VlanCmd(SqCommand):

    def __init__(self, engine: str = '', hostname: str = '',
                 start_time: str = '', end_time: str = '',
                 view: str = 'latest', datacenter: str = '',
                 format: str = "", columns: str = 'default') -> None:
        super().__init__(engine=engine, hostname=hostname,
                         start_time=start_time, end_time=end_time,
                         view=view, datacenter=datacenter,
                         format=format, columns=columns, sqobj=VlanObj)

    @command('show')
    @argument("vlan", description="Space separated list of vlan IDs to show")
    def show(self, vlan: str = ''):
        """
        Show vlan info
        """
        if self.columns is None:
            return

        # Get the default display field names
        now = time.time()
        if self.columns != ['default']:
            self.ctxt.sort_fields = None
        else:
            self.ctxt.sort_fields = []

        df = self.sqobj.get(hostname=self.hostname, vlan=vlan,
                            columns=self.columns, datacenter=self.datacenter)
        self.ctxt.exec_time = "{:5.4f}s".format(time.time() - now)
        return self._gen_output(df)

    @command('summarize')
    @argument("groupby",
              description="Space separated list of fields to summarize on")
    def summarize(self, groupby: str = ''):
        """
        Describe vlan info
        """
        if self.columns is None:
            return

        # Get the default display field names
        now = time.time()
        if self.columns != ['default']:
            self.ctxt.sort_fields = None
        else:
            self.ctxt.sort_fields = []

        df = self.sqobj.summarize(hostname=self.hostname,
                                  columns=self.columns,
                                  groupby=groupby.split(),
                                  datacenter=self.datacenter)
        self.ctxt.exec_time = "{:5.4f}s".format(time.time() - now)
        return self._gen_output(df)
