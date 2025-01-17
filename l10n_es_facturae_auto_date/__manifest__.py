# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'FacturaE auto dates',
    'summary': 'This module computes automatically the FacturaE start date '
               'and end date from date invoice',
    'version': '11.0.1.2.1',
    'category': 'Accounting',
    'author': 'NuoBiT Solutions, S.L., Eric Antones',
    'website': 'https://github.com/nuobit',
    'license': 'AGPL-3',
    'depends': [
        'l10n_es_facturae',
    ],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'development_status': 'Beta',
    'maintainers': ['eantones'],
}
