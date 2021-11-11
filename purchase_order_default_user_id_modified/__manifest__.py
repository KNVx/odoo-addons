# Copyright 2021 NuoBiT Solutions - Kilian Niubo <kniubo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "Purchase Order Default User Id Modified",
    "version": "12.0.1.0.0",
    "author": "NuoBiT Solutions, S.L., Kilian Niubo",
    "license": "AGPL-3",
    "category": "Project",
    "website": "https://github.com/nuobit",
    "summary": "This module allows two fields to indicate who is a bot and who is a default user."
               "This is necessary to set default user in purchase order when it's automated",
    "depends": [
        "base",
        "purchase",
    ],
    "data": ["views/res_users_views.xml", ],
    "installable": True,
}
