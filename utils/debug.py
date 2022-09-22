from timeit import default_timer
import inspect, logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


# NOTE These functions are meant for production and should ONLY be used in development
# environments, this code WILL introduce unecessary overhead if used in live environments


class CodeTimer(object):
    '''A basic context manager for timing code blocks'''
    def __init__(self, repeat: int=100):
        self.timing = 1000 # milliseconds
        self.timer = default_timer
        self.repeat = repeat

    def __enter__(self):
        self.start = self.timer()
        return self.repeat

    def __exit__(self, _exc_type, _exc_val, _traceback):
        end = self.timer()
        self.elapsed = (end - self.start) * self.timing

        log.debug(f"{inspect.stack()[1][3]}'s time: {round(self.elapsed, 6)}ms")


# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
