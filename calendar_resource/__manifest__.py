# -*- coding: utf-8 -*-
# Copyright 2010-2014 Savoir-faire Linux
# Copryight 2017 Laslabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Calendar Resources",
    "summary": "New features to facilitate resource management with meetings.",
    "version": "10.0.1.1.0",
    "category": "CRM",
    "website": "http://www.savoirfairelinux.com",
    "author": "Savoir-faire Linux, LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "resource",
        "calendar",
    ],
    "data": [
        "views/calendar_event_view.xml",
        "views/resource_resource_view.xml",
    ],
    "demo": [
        "demo/resource_resource_demo.xml",
        "demo/resource_calendar.xml",
        "demo/resource_calendar_attendance.xml",
    ],
}
