# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
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

import logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, \
    DEFAULT_SERVER_DATE_FORMAT


from openerp import models, fields, api


class calendar_event(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def create(self, vals):
        event = super(calendar_event, self).create(vals)
        resource_calendar_leave_model = self.env['resource.calendar.leaves']
        model_data_model = self.env['ir.model.data']
        resource_calendar = model_data_model.get_object(
            'calendar_resources', 'resource_calendar'
        )

        ids = []
        for resource in event.resource_ids:
            ids.append(
                resource_calendar_leave_model.create(
                    {
                        'name': 'Meeting : {}'.format(event.name),
                        'calendar_id': resource_calendar.id,
                        'resource_id': resource.id,
                        'date_from': event.start,
                        'date_to': event.stop,
                        'calendar_event_id': event.id,
                    }
                ).id
            )

        event.write({'resource_calendar_leave_ids': ([6, 0, ids],)})

        for leave in event.resource_calendar_leave_ids:
            print 'date_from', leave.date_from
        return event

    resource_ids = fields.Many2many(
        'resource.resource',
        domain="[('display', '=', True)]",
        string='Resources'
    )

    resource_calendar_leave_ids = fields.Many2many(
        'resource.calendar.leaves',
        string='Resources Calendar leaves'
    )

