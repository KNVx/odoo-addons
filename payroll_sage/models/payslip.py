# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class Payslip(models.Model):
    _name = 'payroll.sage.payslip'
    _description = 'Payslip'

    name = fields.Char(string='Name', required=True)
    date = fields.Date(string='Date', required=True)

    labour_agreement_id = fields.Many2one('payroll.sage.labour.agreement', string='Labour agreement',
                                          # domain=[('registration_date_cv', '>=')]
                                          required=True)

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 copy=False, default=lambda self: self.env['res.company']._company_default_get())

    type = fields.Selection([('transfer', _('Transfer')), ('payroll', _('Payroll'))], string='Type', required=True)

    ss_cost = fields.Float('S.S. cost')

    payment_date = fields.Date('Payment date')

    note = fields.Text(string='Note')

    payslip_line_ids = fields.One2many('payroll.sage.payslip.line',
                                       'payslip_id', string='Wage types', copy=True)

    payslip_check_ids = fields.One2many('payroll.sage.payslip.check',
                                        'payslip_id', string='Checks', copy=True)

    state = fields.Selection([
        ('draft', _('Draft')),
        ('validated', _('Validated')),
        ('posted', _('Posted')),
    ], string='Status', default='draft', readonly=True, required=True, copy=False)

    @api.multi
    def action_paysplip_validate(self):
        self.write({'state': 'validated'})

    @api.multi
    def action_paysplip_set_to_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_paysplip_post(self):
        self.write({'state': 'posted'})

    @api.multi
    def action_paysplip_unpost(self):
        self.write({'state': 'validated'})


class PayslipLine(models.Model):
    _name = 'payroll.sage.payslip.line'
    _description = 'Payslip line'

    name = fields.Char('Description')

    wage_type_line_id = fields.Many2one('payroll.sage.labour.agreement.wage.type.line',
                                        string='Wage type line', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)

    amount = fields.Float('Amount', required=True)

    payslip_id = fields.Many2one('payroll.sage.payslip', string='Payslip', required=True)


class PayslipCheck(models.Model):
    _name = 'payroll.sage.payslip.check'
    _description = 'Payslip check'

    name = fields.Char('Description')

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)

    amount = fields.Float('Amount', required=True)

    payslip_id = fields.Many2one('payroll.sage.payslip', string='Payslip', required=True)
