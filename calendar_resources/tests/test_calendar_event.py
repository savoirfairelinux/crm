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
        self.model_data_model = self.env['ir.model.data']
        self.resource_calendar = self.model_data_model.get_object(
            'calendar_resources', 'resource_calendar'
        )
        self.calendar_event_model = self.env['calendar.event']
        self.resource_resource_model = self.env['resource.resource']
        self.resource_calendar_leaves_model = self.env[
            'resource.calendar.leaves'
        ]

    @property
    def _event_with_resources(self):
        resources = [
            self.resource_resource_model.create({
                'name': 't_resource1',
                'calendar_id': self.resource_calendar.id,
                'code': 666,
            }),
            self.resource_resource_model.create({
                'name': 't_resource2',
                'calendar_id': self.resource_calendar.id,
                'code': 111,
            }),
        ]
        return self.calendar_event_model.create(
            {
                'name': 't_name',
                'start_datetime': '2011-11-11 00:00:00',
                'stop_datetime': '2011-11-11 00:00:00',
                'allday': True,
                'resource_ids': (
                    [
                        6, False,
                        [resource.id for resource in resources]
                    ],
                ),
            }
        )

    def test_there_is_resource_calendar_id1(self):
        """ It is assumed the resource calendar id 1 exists in the create
        method.
        """
        self.assertTrue(self.resource_calendar)

    def test_create_adds_related_resource_calendar_leaves(self):
        """ When a calendar event is created with resource(s) related to it
        the resource calendar should be fed with new leaves.
        """
        self.assertTrue(self._event_with_resources.resource_calendar_leave_ids)

    def test_new_leaves_have_event(self):
        """ Double check the created leaves got the event. """
        for leave in self._event_with_resources.resource_calendar_leave_ids:
            self.assertTrue(leave.calendar_event_id)

    def test_leaves_and_event_same_dates(self):
        """ Double checking the leaves inherit the dates of the event."""
        event = self._event_with_resources

        for leave in event.resource_calendar_leave_ids:
            self.assertEqual(leave.date_from, event.start)
            self.assertEqual(leave.date_to, event.stop)

