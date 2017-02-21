import sys


class progressbar(object):
    def __init__(self, final_count, show_text='Progress', block_char='*'):
        self.final_count = final_count
        self.block_count = 0
        self.block = block_char
        self.f = sys.stdout
        if not self.final_count:
            return
        self.f.write(show_text + ': ')

    def progress(self, count):
        count = min(count, self.final_count)
        if self.final_count:
            percent_complete = int(round(100.0 * count / self.final_count))
            if percent_complete < 1:
                percent_complete = 1
        else:
            percent_complete = 100
        block_count = int(percent_complete // 2)
        if block_count <= self.block_count:
            return
        for i in range(self.block_count, block_count):
            self.f.write(self.block)
        self.f.flush()
        self.block_count = block_count
        if percent_complete == 100:
            self.f.write(" Complete!\n")

