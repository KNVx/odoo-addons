# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models, fields

from odoo.addons.component.core import Component
from odoo.addons.queue_job.job import job


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sage_bind_ids = fields.One2many(
        comodel_name='sage.hr.employee',
        inverse_name='odoo_id',
        string='Sage Bindings',
    )


class HrEmployeeBinding(models.Model):
    _name = 'sage.hr.employee'
    _inherit = 'sage.binding'
    _inherits = {'hr.employee': 'odoo_id'}

    odoo_id = fields.Many2one(comodel_name='hr.employee',
                              string='Employee',
                              required=True,
                              ondelete='cascade')

    ## composed id
    sage_codigo_empresa = fields.Integer(string="CodigoEmpresa", required=True)
    sage_codigo_empleado = fields.Integer(string="CodigoEmpleado", required=True)

    _sql_constraints = [
        ('uniq', 'unique(odoo_id, sage_codigo_empresa, sage_codigo_empleado)',
         'Empllyee with same ID on Sage already exists.'),
    ]

    @job(default_channel='root.sage')
    def import_employees_since(self, backend_record=None, since_date=None):
        """ Prepare the import of employees modified on Sage """
        filters = {
            'CodigoEmpresa': backend_record.sage_company_id,
        }
        now_fmt = fields.Datetime.now()
        self.env['sage.hr.employee'].import_batch(
            backend=backend_record, filters=filters)
        backend_record.import_employees_since_date = now_fmt

        return True
