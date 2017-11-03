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

sleep_duration = None

mock_file_index_list = ['../data/test_file_0.h5', '../data/test_file_1.h5',
                        '../data/test_file_9.h5']

# TODO auto generate with bin/gen_rand_data.py
mock_sample_specification = [
    ['../data/test_file_0.h5', ['tensor_1', 'tensor_2'], 'class_1', 1],
    ['../data/test_file_1.h5', ['tensor_1', 'tensor_2'], 'class_2', 2],
    ['../data/test_file_9.h5', ['tensor_1', 'tensor_2'], 'class_10', 10]
]

expected_class_count = 3

mock_expected_malloc_requests = [('tensor_1', (5,)),
                                 ('tensor_2', (5,))]

mock_one_hot = [('class_index', tuple()),
                ('one_hot', (3,))]

mock_file_index_malloc = [('class_index', tuple()),
                          ('one_hot', (3,)),
                          ('file_struct', (2,))]

mock_class_index_map = {
    'class_1' : 0,
    'class_2' : 1,
    'class_10': 2
}

# mock_classes = {
#     'class_2': {'class_prob': 0.15384615384615385, 'file_index': 0,
#                 'data_set_names': ['tensor_1', 'tensor_2'],
#                 'file_handle': False, 'example_index': 0,
#                 'file_names': ['../data/test_file_1.h5'],
#                 'current_file_indecies': None, 'class_index': 1,
#                 'n_examples': 0, 'N': 0},
#     'class_1': {'class_prob': 0.07692307692307693, 'file_index': 0,
#                 'data_set_names': ['tensor_1', 'tensor_2'],
#                 'file_handle': False, 'example_index': 0,
#                 'file_names': ['../data/test_file_0.h5'],
#                 'current_file_indecies': None, 'class_index': 0,
#                 'n_examples': 0, 'N': 0},
#     'class_10': {'class_prob': 0.7692307692307693, 'file_index': 0,
#                  'data_set_names': ['tensor_1', 'tensor_2'],
#                  'file_handle': False, 'example_index': 0,
#                  'file_names': ['../data/test_file_9.h5'],
#                  'current_file_indecies': None, 'class_index': 2,
#                  'n_examples': 0, 'N': 0}}

mock_classes = {
    'class_1' : {'class_prob'          : 0.07692307692307693,
                 'file_index'          : 0,
                 'data_set_names'      : ['tensor_1', 'tensor_2'],
                 'file_handle'         : False,
                 'example_index'       : 0,
                 'current_file_indices': None,
                 'file_names'          : [0],
                 'class_index'         : 0,
                 'n_examples'          : 0},
    'class_10': {'class_prob'          : 0.7692307692307693,
                 'file_index'          : 0,
                 'data_set_names'      : ['tensor_1', 'tensor_2'],
                 'file_handle'         : False,
                 'example_index'       : 0,
                 'current_file_indices': None,
                 'file_names'          : [2],
                 'class_index'         : 2,
                 'n_examples'          : 0},
    'class_2' : {'class_prob'          : 0.15384615384615385,
                 'file_index'          : 0,
                 'data_set_names'      : ['tensor_1', 'tensor_2'],
                 'file_handle'         : False,
                 'example_index'       : 0,
                 'current_file_indices': None,
                 'file_names'          : [1],
                 'class_index'         : 1,
                 'n_examples'          : 0}
}

mock_batches = [[(1, ['tensor_1', 'tensor_2'], 'class_2', (0, 163), 0),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (0, 73), 0),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (0, 764), 0)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (163, 352), 1),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (73, 145), 1),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (764, 1503), 1)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (352, 510), 2),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (145, 217), 2),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (1503, 1999), 2),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (0, 274), 2)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (510, 657), 3),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (217, 295), 3),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (274, 1049), 3)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (657, 816), 4),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (295, 370), 4),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (1049, 1815), 4)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (816, 975), 5),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (370, 438), 5),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (1815, 1999), 5),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (0, 589), 5)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (975, 1121), 6),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (438, 512), 6),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (589, 1369), 6)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (1121, 1279), 7),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (512, 584), 7),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (1369, 1999), 7),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (0, 140), 7)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (1279, 1429), 8),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (584, 655), 8),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (140, 919), 8)],
                [(1, ['tensor_1', 'tensor_2'], 'class_2', (1429, 1579), 9),
                 (0, ['tensor_1', 'tensor_2'], 'class_1', (655, 737), 9),
                 (2, ['tensor_1', 'tensor_2'], 'class_10', (919, 1687), 9)]]

mock_data_sets = ['tensor_1', 'tensor_2']

mock_read_batches = [(0, 0, ['tensor_1', 'tensor_2']),
                     (0, 1, ['tensor_1', 'tensor_2']),
                     (0, 2, ['tensor_1', 'tensor_2']),
                     (0, 3, ['tensor_1', 'tensor_2']),
                     (0, 4, ['tensor_1', 'tensor_2'])]

# I apologize in advance...
mock_filtered_batches = [[(1, ['tensor_1', 'tensor_2'], 'class_2',
                           [1000, 1002, 1004, 1006, 1008, 1010, 1012, 1014,
                            1016, 1018, 1020, 1022, 1024, 1026, 1028, 1030,
                            1032, 1034, 1036, 1038, 1040, 1042, 1044, 1046,
                            1048, 1050, 1052, 1054, 1056, 1058, 1060, 1062,
                            1064], 0),
                          (0, ['tensor_1', 'tensor_2'], 'class_1',
                           [1000, 1002, 1004, 1006, 1008, 1010, 1012, 1014, 1016,
                            1018, 1020, 1022, 1024, 1026, 1028, 1030, 1032, 1034,
                            1036, 1038], 0),
                          (2, ['tensor_1', 'tensor_2'], 'class_10',
                           [1000, 1002, 1004, 1006, 1008, 1010, 1012, 1014, 1016,
                            1018, 1020, 1022, 1024, 1026, 1028, 1030, 1032, 1034,
                            1036, 1038, 1040, 1042, 1044, 1046, 1048, 1050, 1052,
                            1054, 1056, 1058, 1060, 1062, 1064, 1066, 1068, 1070,
                            1072, 1074, 1076, 1078, 1080, 1082, 1084, 1086, 1088,
                            1090, 1092, 1094, 1096, 1098, 1100, 1102, 1104, 1106,
                            1108, 1110, 1112, 1114, 1116, 1118, 1120, 1122, 1124,
                            1126, 1128, 1130, 1132, 1134, 1136, 1138, 1140, 1142,
                            1144, 1146, 1148, 1150, 1152, 1154, 1156, 1158, 1160,
                            1162, 1164, 1166, 1168, 1170, 1172, 1174, 1176, 1178,
                            1180, 1182, 1184, 1186, 1188, 1190, 1192, 1194, 1196,
                            1198, 1200, 1202, 1204, 1206, 1208, 1210, 1212, 1214,
                            1216, 1218, 1220, 1222, 1224, 1226, 1228, 1230, 1232,
                            1234, 1236, 1238, 1240, 1242, 1244, 1246, 1248, 1250,
                            1252, 1254, 1256, 1258, 1260, 1262, 1264, 1266, 1268,
                            1270, 1272, 1274, 1276, 1278, 1280, 1282, 1284, 1286,
                            1288, 1290, 1292], 0)],
                         [(1, ['tensor_1', 'tensor_2'], 'class_2',
                           [1066, 1068, 1070, 1072, 1074, 1076, 1078, 1080, 1082, 1084, 1086, 1088,
                            1090, 1092, 1094, 1096, 1098, 1100, 1102, 1104, 1106, 1108, 1110, 1112,
                            1114, 1116, 1118, 1120, 1122, 1124, 1126, 1128, 1130, 1132], 1),
                          (0, ['tensor_1', 'tensor_2'], 'class_1',
                           [1040, 1042, 1044, 1046, 1048, 1050, 1052, 1054, 1056, 1058, 1060, 1062,
                            1064, 1066, 1068], 1),
                          (2, ['tensor_1', 'tensor_2'], 'class_10',
                           [1294, 1296, 1298, 1300, 1302, 1304, 1306, 1308, 1310, 1312, 1314, 1316,
                            1318, 1320, 1322, 1324, 1326, 1328, 1330, 1332, 1334, 1336, 1338, 1340,
                            1342, 1344, 1346, 1348, 1350, 1352, 1354, 1356, 1358, 1360, 1362, 1364,
                            1366, 1368, 1370, 1372, 1374, 1376, 1378, 1380, 1382, 1384, 1386, 1388,
                            1390, 1392, 1394, 1396, 1398, 1400, 1402, 1404, 1406, 1408, 1410, 1412,
                            1414, 1416, 1418, 1420, 1422, 1424, 1426, 1428, 1430, 1432, 1434, 1436,
                            1438, 1440, 1442, 1444, 1446, 1448, 1450, 1452, 1454, 1456, 1458, 1460,
                            1462, 1464, 1466, 1468, 1470, 1472, 1474, 1476, 1478, 1480, 1482, 1484,
                            1486, 1488, 1490, 1492, 1494, 1496, 1498, 1500, 1502, 1504, 1506, 1508,
                            1510, 1512, 1514, 1516, 1518, 1520, 1522, 1524, 1526, 1528, 1530, 1532,
                            1534, 1536, 1538, 1540, 1542, 1544, 1546, 1548, 1550, 1552, 1554, 1556,
                            1558, 1560, 1562, 1564, 1566, 1568, 1570, 1572, 1574, 1576, 1578, 1580,
                            1582, 1584, 1586, 1588, 1590, 1592, 1594], 1)],
                         [(1, ['tensor_1', 'tensor_2'], 'class_2',
                           [1134, 1136, 1138, 1140, 1142, 1144, 1146, 1148, 1152, 1154, 1156, 1158,
                            1160, 1162, 1164, 1166, 1168, 1170, 1172, 1174, 1176, 1178, 1180, 1182,
                            1184, 1186, 1188, 1190, 1192, 1194, 1196, 1198, 1202, 1204, 1206], 2),
                          (0, ['tensor_1', 'tensor_2'], 'class_1',
                           [1070, 1072, 1074, 1076, 1078, 1080, 1082, 1084, 1086, 1088, 1090, 1092,
                            1094, 1096, 1098, 1100, 1102, 1104], 2),
                          (2, ['tensor_1', 'tensor_2'], 'class_10',
                           [1596, 1598, 1600, 1602, 1604, 1606, 1608, 1610, 1612, 1614, 1616, 1618,
                            1620, 1622, 1624, 1626, 1628, 1630, 1632, 1634, 1636, 1638, 1640, 1642,
                            1644, 1646, 1648, 1650, 1652, 1654, 1656, 1658, 1660, 1662, 1664, 1666,
                            1668, 1670, 1672, 1674, 1676, 1678, 1680, 1682, 1684, 1686, 1688, 1690,
                            1692, 1694, 1696, 1698, 1700, 1702, 1704, 1706, 1708, 1710, 1712, 1714,
                            1716, 1718, 1720, 1722, 1724, 1726, 1728, 1730, 1732, 1734, 1736, 1738,
                            1740, 1742, 1744, 1746, 1748, 1750, 1752, 1754, 1756, 1758, 1760, 1762,
                            1764, 1766, 1768, 1770, 1772, 1774, 1776, 1778, 1780, 1782, 1784, 1786,
                            1788, 1790, 1792, 1794, 1796, 1798, 1800, 1802, 1804, 1806, 1808, 1810,
                            1812, 1814, 1816, 1818, 1820, 1822, 1824, 1826, 1828, 1830, 1832, 1834,
                            1836, 1838, 1840, 1842, 1844, 1846, 1848, 1850, 1852, 1854, 1856, 1858,
                            1860, 1862, 1864, 1866, 1868, 1870, 1872, 1874, 1876, 1878, 1880, 1882,
                            1884, 1886, 1888], 2)]]
