# -*- coding: utf-8 -*-
# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Contract Payment Mode Purchase',
    'summary': 'Payment mode in contracts and their invoices for purchases',
    'version': '10.0.0.1.0',
    'author': 'NuoBiT Solutions, S.L., Eric Antones',
    'website': 'https://www.nuobit.com',
    'category': 'Contract Management',
    'license': 'AGPL-3',
    'depends': [
        'contract_purchase',
        'contract_payment_mode'
    ],
    'data': [
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': True,
}
