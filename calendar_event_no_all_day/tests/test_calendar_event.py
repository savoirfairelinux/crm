# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from openerp.tests import common


class test_calendar_event(common.TransactionCase):
    def setUp(self):
        super(test_calendar_event, self).setUp()
        self.calendar_event_model = self.env['calendar.event']

    def test_all_day_false_after_create(self):
        event = self.calendar_event_model.create(
            {'name': 't_name', 'allday': True, }
        )
        self.assertFalse(event.allday)
