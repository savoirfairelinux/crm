# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Savoir-faire Linux
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

from openerp import models, fields, api, tools
from openerp import osv


class resource_resource(models.Model):
    _inherit = 'resource.resource'

    @api.multi
    def _get_image(self, name, args):
        return dict(
            (p.id, tools.image_get_resized_images(p.image)) for p in self)

    @api.one
    def _set_image(self, name, value, args):
        return self.write({'image': tools.image_resize_image_big(value)})

    _store_image = {'resource.resource': (
        lambda self, cr, uid, ids, c={}: ids, ['image'], 10
    ),
                    }

    name = fields.Char("Name", required=True, translate=True)
    image = fields.Binary(
        "Image",
        help="This field holds the image used as avatar for this contact,"
             " limited to 1024x1024px"
    )

    # dirty, but no time to learn v8 function style
    _columns = {
        'image_medium': osv.fields.function(
            _get_image,
            fnct_inv=_set_image,
            string="Medium-sized photo",
            type="binary", multi="_get_image",
            store=_store_image,
            help="Medium-sized image of this publication. It is automatically "
                 "resized as a 128x128px image, with aspect ratio preserved. "
                 "Use this field in form views or some kanban views.."
        )
    }

    display = fields.Boolean(default=True)
    note = fields.Text()
