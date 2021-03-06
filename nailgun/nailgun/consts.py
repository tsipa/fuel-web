# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from collections import namedtuple


def Enum(*values, **kwargs):
    names = kwargs.get('names')
    if names:
        return namedtuple('Enum', names)(*values)
    return namedtuple('Enum', values)(*values)

RELEASE_STATES = Enum(
    'not_available',
    'downloading',
    'error',
    'available'
)

NETWORK_INTERFACE_TYPES = Enum(
    'ether',
    'bond'
)

OVS_BOND_MODES = Enum(
    'active-backup',
    'balance-slb',
    'lacp-balance-tcp',
    names=(
        'active_backup',
        'balance_slb',
        'lacp_balance_tcp',
    )
)
