#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# yapf: disable
# type: ignore



checkname = 'ibm_svc_mdisk'


info = [[u'0',
         u'stp5_300G_01-01',
         u'online',
         u'managed',
         u'16',
         u'stp5_300G_01',
         u'1.1TB',
         u'0000000000000000',
         u'BLUBB5',
         u'6  00a0b80006e1dbc0000f6f9513026a000000000000000000000000000000000',
         u'generic_hdd'],
        [u'1',
         u'Quorum_BLUBB3',
         u'online',
         u'managed',
         u'0',
         u'Quorum_2',
         u'1.0GB',
         u'0000000000000000',
         u'BLUBB3',
         u'600a0b80  00293eb800001f264c3e8a1f00000000000000000000000000000000',
         u'generic_hdd'],
        [u'2',
         u'stp6_300G_01-01',
         u'online',
         u'managed',
         u'15',
         u'stp6_300G_01',
         u'1.1TB',
         u'0000000000000000',
         u'BLUBB6',
         u'6  00a0b80006e8e3c00000f1651302b8800000000000000000000000000000000',
         u'generic_hdd'],
        [u'3',
         u'Quorum_blubb5',
         u'online',
         u'managed',
         u'18',
         u'Quorum_0',
         u'1.0GB',
         u'0000000000000001',
         u'BLUBB5',
         u'600a0b8  0006e1dcc0000f6905130225800000000000000000000000000000000',
         u'generic_hdd'],
        [u'4',
         u'Quorum_blubb6',
         u'online',
         u'managed',
         u'17',
         u'Quorum_1',
         u'1.0GB',
         u'0000000000000001',
         u'BLUBB6',
         u'600a0b8  0006e1d5e00000dcb5130228700000000000000000000000000000000',
         u'generic_hdd'],
        [u'5',
         u'stp5_300G_01-02',
         u'online',
         u'managed',
         u'16',
         u'stp5_300G_01',
         u'1.1TB',
         u'0000000000000002',
         u'BLUBB5',
         u'6  00a0b80006e1dbc0000f6fc51304bfc00000000000000000000000000000000',
         u'generic_hdd'],
        [u'6',
         u'stp6_300G_01-02',
         u'online',
         u'managed',
         u'15',
         u'stp6_300G_01',
         u'1.1TB',
         u'0000000000000002',
         u'BLUBB6',
         u'6  00a0b80006e8e3c00000f1951304f9a00000000000000000000000000000000',
         u'generic_hdd'],
        [u'7',
         u'stp5_300G_01-03',
         u'online',
         u'managed',
         u'16',
         u'stp5_300G_01',
         u'1.1TB',
         u'0000000000000003',
         u'BLUBB5',
         u'6  00a0b80006e1dcc0000f76951305bc000000000000000000000000000000000',
         u'generic_hdd'],
        [u'8',
         u'stp6_300G_01-03',
         u'online',
         u'managed',
         u'15',
         u'stp6_300G_01',
         u'1.1TB',
         u'0000000000000003',
         u'BLUBB6',
         u'6  00a0b80006e1d5e00000e9a51305a3200000000000000000000000000000000',
         u'generic_hdd'],
        [u'9',
         u'stp5_300G_01-04',
         u'online',
         u'managed',
         u'16',
         u'stp5_300G_01',
         u'1.1TB',
         u'0000000000000004',
         u'BLUBB5',
         u'6  00a0b80006e1dbc0000f7d051341cc000000000000000000000000000000000',
         u'generic_hdd']]


discovery = {'': [(u'Quorum_BLUBB3', {}),
                  (u'Quorum_blubb5', {}),
                  (u'Quorum_blubb6', {}),
                  (u'stp5_300G_01-01', {}),
                  (u'stp5_300G_01-02', {}),
                  (u'stp5_300G_01-03', {}),
                  (u'stp5_300G_01-04', {}),
                  (u'stp6_300G_01-01', {}),
                  (u'stp6_300G_01-02', {}),
                  (u'stp6_300G_01-03', {})]}


checks = {'': [(u'Quorum_BLUBB3',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'Quorum_blubb5',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'Quorum_blubb6',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'stp5_300G_01-01',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'stp5_300G_01-02',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'stp5_300G_01-03',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'stp5_300G_01-04',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'stp6_300G_01-01',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'stp6_300G_01-02',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])]),
               (u'stp6_300G_01-03',
                {'array_mode': 0,
                 'degraded_state': 1,
                 'excluded_state': 2,
                 'image_mode': 0,
                 'managed_mode': 0,
                 'offline_state': 2,
                 'online_state': 0,
                 'unmanaged_mode': 1},
                [(0, u'Status: online', []), (0, u'Mode: managed', [])])]}
