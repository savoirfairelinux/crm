# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
# (<http://www.savoirfairelinux.com>).
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
    def _create_resource_calendar_leaves(self, event):
        resource_calendar_leaves_model = self.env['resource.calendar.leaves']
        model_data_model = self.env['ir.model.data']
        resource_calendar = model_data_model.get_object(
            'calendar_resources', 'resource_calendar'
        )

        ids = []
        for resource in event.resource_ids:
            ids.append(
                resource_calendar_leaves_model.create(
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

        event.write({'resource_calendar_leaves_ids': ([6, 0, ids],)})

        return event.resource_calendar_leaves_ids

    @api.model
    def create(self, vals):
        """ Create the event then create resource leaves linked to the
        resources used by the event.
        """
        event = super(calendar_event, self).create(vals)
        self._create_resource_calendar_leaves(event)
        return event

    @api.multi
    def write(self, vals):
        """ Update the leaves related to the event."""
        # easier to delete all leaves currently related to the event,
        # as otherwise we would have to test a lot of parameter.
        for leaf in self.resource_calendar_leaves_ids:
            leaf.unlink()

        # and then just recreate them
        self._create_resource_calendar_leaves(self)
        return super(calendar_event, self).write(vals)

    resource_ids = fields.Many2many(
        'resource.resource',
        domain="[('display', '=', True)]",
        string='Resources'
    )

    resource_calendar_leaves_ids = fields.Many2many(
        'resource.calendar.leaves',
        string='Resources Calendar leaves'
    )

