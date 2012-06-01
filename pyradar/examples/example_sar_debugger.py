# -*- coding: utf-8 -*-
from pyradar.utils.sar_debugger import take_snapshot

MAX_ITER = 1000

for iter in xrange(0, MAX_ITER):
    image = some_algorithm(image)
    take_snapshot(image, iteration_step=iter)
