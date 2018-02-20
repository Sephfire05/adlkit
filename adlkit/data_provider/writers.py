# -*- coding: utf-8 -*-
"""
ADLKit
Copyright ©2017 AnomalousDL, Inc.  All rights reserved.

AnomalousDL, Inc. (ADL) licenses this file to you under the Academic and Research End User License Agreement (the
"License"); you may not use this file except in compliance with the License.  You may obtain a copy of the License at

  http://www.anomalousdl.com/licenses/ACADEMIC-LICENSE.txt

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL ADL BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE, either express
or implied.  See the License for the specific language governing permissions and limitations under the License.
"""

import collections
import logging as lg

import os
import time
from future.utils import raise_with_traceback

from adlkit.data_provider.comm_drivers import BaseCommDriver
from adlkit.data_provider.config import WRITER_OFFSET
from adlkit.data_provider.io_drivers import IOController
from adlkit.data_provider.workers import Worker

writer_lg = lg.getLogger('data_provider.workers.writers')


# writer_lg.setLevel(lg.DEBUG)


class BaseWriter(Worker):
    data_src = None
    data_dst = None

    current_handle = None
    meta = None

    complete = None

    def __init__(self,
                 io_ctlr,
                 worker_id, comm_driver, data_src, data_dst,
                 read_batches_per_epoch=None,
                 pre_write_function=None,
                 meta=None,

                 max_batches=None,
                 sleep_duration=1,
                 **kwargs):

        super(BaseWriter, self).__init__(worker_id=worker_id + WRITER_OFFSET,
                                         comm_driver=comm_driver,
                                         sleep_duration=sleep_duration,
                                         **kwargs)

        assert isinstance(comm_driver, BaseCommDriver)
        assert isinstance(io_ctlr, IOController)
        assert isinstance(data_src, collections.Iterable)
        self.io_ctlr = io_ctlr
        self.data_src = data_src
        self.data_dst = data_dst
        self.read_batches_per_epoch = read_batches_per_epoch
        self.pre_write_function = pre_write_function
        self.meta = meta or dict()

        self.max_batches = max_batches

    def debug(self, message):
        if isinstance(message, list):
            message = " ".join(message)
        writer_lg.debug(" writer_id={0} ".format(self.worker_id) + message)

    def info(self, message):
        if isinstance(message, list):
            message = " ".join(message)
        writer_lg.info(" writer_id={0} writer_batch_id={1} ".format(self.worker_id,
                                                                    self.batch_count) + message)

    def critical(self, message):
        if isinstance(message, list):
            message = " ".join(message)
        writer_lg.critical(" writer_id={0} writer_batch_id={1} ".format(self.worker_id,
                                                                        self.batch_count) + message)

    def error(self, message):
        if isinstance(message, list):
            message = " ".join(message)
        writer_lg.error(" writer_id={0} writer_batch_id={1} ".format(self.worker_id,
                                                                     self.batch_count) + message)

    def run(self, **kwargs):
        self.write()

    def write(self):
        self.debug('starting...')

        # TODO - wghilliard - MORE BETTER PLS
        lock_file_name = self.data_dst + '.lock'
        with open(lock_file_name, 'a'):
            self.debug("writing lock_file={}".format(lock_file_name))
            pass

        with self.io_ctlr:
            io_driver = self.io_ctlr(self.data_dst.split('.')[-1])
            with io_driver:
                self.current_handle = io_driver.put(self.data_dst, read_batches_per_epoch=self.read_batches_per_epoch)

                next_datum_time = time.time()
                while not self.should_stop():
                    try:
                        payload = next(self.data_src)
                    except StopIteration:
                        self.debug(' StopIteration received...')
                        break
                    except Exception as e:
                        raise_with_traceback(e)

                    self.debug("next_datum_time_wait_time={0}".format(time.time() - next_datum_time))

                    # descriptor, datum = payload
                    # TODO - wghilliard - more better dataset naming
                    descriptor, datum = 'cache', payload

                    write_function_time = time.time()
                    if self.pre_write_function:
                        datum = self.pre_write_function(datum)
                    self.debug(" write_function_time={0}".format(time.time() - write_function_time))

                    datum_write_time = time.time()
                    self.current_handle[descriptor] = datum
                    self.debug(" datum_write_time={0}".format(time.time() - datum_write_time))

                    self.batch_count += 1
                    self.debug(" wrote={}/{}".format(self.batch_count, self.max_batches))
                    next_datum_time = time.time()
            io_driver.close(self.data_dst, self.current_handle, force=True)

        self.debug("removing lock_file={}".format(lock_file_name))
        os.remove(lock_file_name)
        self.debug("exiting...")
        self.seppuku()
