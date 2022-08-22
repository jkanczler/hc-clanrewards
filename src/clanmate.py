class ClanMate:
    def __init__(self, init_obj):
        self.name = init_obj['name']
        self.glory = init_obj['glory']
        self.demands = init_obj['demands']
        self.received = []
        self.received_display = ''

        for demand in self.demands:
            demand['original'] = demand['quantity']
