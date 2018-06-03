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
import datetime

import attr
from adlkit_internal.common.utils import get_new_uid


@attr.s(slots=True)
class DataPoint(object):
    source_name = attr.ib(converter=str)
    source_type = attr.ib(converter=str)
    index = attr.ib(converter=str)

    data_set_list = attr.ib()

    uid = attr.ib(default=attr.Factory(get_new_uid), converter=str)
    timestamp = attr.ib(default=attr.Factory(datetime.datetime.utcnow), type=datetime.datetime)


@attr.s(slots=True)
class LabelInstance(object):
    data_point_uid = attr.ib(converter=str)
    label_uid = attr.ib(converter=str)

    uid = attr.ib(default=attr.Factory(get_new_uid), converter=str)
    timestamp = attr.ib(default=attr.Factory(datetime.datetime.utcnow), type=datetime.datetime)


@attr.s(slots=True)
class Label(object):
    name = attr.ib(converter=str)
    comment = attr.ib(converter=str, default='')
    is_origin = attr.ib(type=bool, default=False)

    uid = attr.ib(default=attr.Factory(get_new_uid), converter=str)
    timestamp = attr.ib(default=attr.Factory(datetime.datetime.utcnow), type=datetime.datetime)
