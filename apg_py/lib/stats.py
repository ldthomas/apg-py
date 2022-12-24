''' @file apg_py/lib/stats.py @brief Collects parser's node statistics.'''
from apg_py.lib import identifiers as id


class Stats():
    def __init__(self, parser):
        '''Class constructor.
        @param parser the parser object to attach this Stats object to'''
        self.parser = parser
        parser.stats = self
        self.stats = {}
        self.rule_stats = {}
        self.names = {}
        for rule in self.parser.rules:
            self.names[rule['lower']] = rule['name']
        for udt in self.parser.udts:
            self.names[udt['lower']] = udt['name']
        self.clear()

    def clear(self):
        '''For internal use.
        Called here and by the parser to initialize the hit counts.'''
        s = {id.EMPTY: 0, id.MATCH: 0, id.NOMATCH: 0}
        self.stats[id.ALT] = s.copy()
        self.stats[id.CAT] = s.copy()
        self.stats[id.REP] = s.copy()
        self.stats[id.RNM] = s.copy()
        self.stats[id.TLS] = s.copy()
        self.stats[id.TBS] = s.copy()
        self.stats[id.TRG] = s.copy()
        self.stats[id.UDT] = s.copy()
        self.stats[id.AND] = s.copy()
        self.stats[id.NOT] = s.copy()
        self.stats[id.BKR] = s.copy()
        self.stats[id.BKA] = s.copy()
        self.stats[id.BKN] = s.copy()
        self.stats[id.ABG] = s.copy()
        self.stats[id.AEN] = s.copy()
        for name in self.names:
            self.rule_stats[name] = s.copy()

    def total(self, stat):
        '''For internal use. Computes the total number of hits.'''
        return stat[id.EMPTY] + stat[id.MATCH] + stat[id.NOMATCH]

    def collect(self, op):
        '''Called by the parser for each node to collect the hit count.'''
        state = self.parser.state
        self.stats[op['type']][state] += 1
        if(op['type'] == id.RNM):
            rule = self.parser.rules[op['index']]
            self.rule_stats[rule['lower']][state] += 1
        if(op['type'] == id.UDT):
            udt = self.parser.udts[op['index']]
            self.rule_stats[udt['lower']][state] += 1

    def display(self):
        '''Display the parse tree node hit statistics.
        It will first display the node statistics for the various
        node operators.
        It then displays the rule name and UDT name statistics.
        Operators and rule/UDT names for which the hit count is 0 are
        not displayed.'''
        mTotal = 0
        eTotal = 0
        nTotal = 0
        tTotal = 0
        # display operator stats
        print('        OPERATOR NODE HIT STATISTICS')
        print(
            '%5s %7s %7s %7s %7s' %
            ('', 'MATCH', 'EMPTY', 'NOMATCH', 'TOTAL'))
        for stat_id in self.stats:
            stat = self.stats[stat_id]
            total = self.total(stat)
            if(total):
                # ignore operators with no hits
                print('%5s' % (id.dict.get(stat_id)) + ' ', end='')
                mTotal += stat[id.MATCH]
                eTotal += stat[id.EMPTY]
                nTotal += stat[id.NOMATCH]
                tTotal += total
                p = '%7d %7d %7d %7d' % (
                    stat[id.MATCH], stat[id.EMPTY], stat[id.NOMATCH], total)
                print(p)
        print('%5s ' % ('TOTAL'), end='')
        p = '%7d %7d %7d %7d' % (
            mTotal, eTotal, nTotal, tTotal)
        print(p)
        print()
        print('  RULE NAME (RNM/UDT) NODE HIT STATISTICS')
        print(
            '%7s %7s %7s %7s %s' %
            ('MATCH', 'EMPTY', 'NOMATCH', 'TOTAL', 'RULE/UDT NAME'))

        def by_name(val):
            return val[0]

        def by_count(val):
            return val[1]

        # display rule stats
        # order rules alphabetically and then by number of hits,
        # ignoring those with no hits
        ll = []
        for name in self.rule_stats:
            stat = self.rule_stats[name]
            ll.append((name, self.total(stat)))

        ll.sort(key=by_name)
        ll.sort(key=by_count, reverse=True)
        for item in ll:
            count = item[1]
            if(count):
                name = item[0]
                stat = self.rule_stats[name]
                p = '%7d %7d %7d %7d %s' % (
                    stat[id.MATCH], stat[id.EMPTY], stat[id.NOMATCH],
                    count, self.names[name])
                print(p)
