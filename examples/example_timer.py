#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyradar.utils.timeutils import Timer

# crea y arranca el timer
simple_timer = Timer()
# procedimiento que queremos medir
result = function(arg1, arg2)
# paramos el timer
simple_timer.stop_timer()
#imprimimos los resultados y los guardamos en diff
diff = simple_timer.calculate_time_elapsed(print_value=True)

