# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime


class AccountLineInh(models.Model):
    _inherit = 'account.analytic.line'

    planned_hours = fields.Float('Planned Hours', related='task_id.planned_hours')
    billed_hours = fields.Float('Billed Hours')
    total_cost = fields.Float(string="Total Cost",)

    def action_compute_cost(self):
        for rec in self:
            rec.total_cost = rec.employee_id.contract_id.total_Cost_hour * rec.unit_amount


class AccountPaymentRegisterInh(models.TransientModel):
    _inherit = 'account.payment.register'
#
#     # def _create_payments(self):
#     #     print('hhh')
#     #     self.ensure_one()
#     #     batches = self._get_batches()
#     #     edit_mode = self.can_edit_wizard and (len(batches[0]['lines']) == 1 or self.group_payment)
#     #     to_process = []
#     #
#     #     if edit_mode:
#     #         payment_vals = self._create_payment_vals_from_wizard()
#     #         to_process.append({
#     #             'create_vals': payment_vals,
#     #             'to_reconcile': batches[0]['lines'],
#     #             'batch': batches[0],
#     #         })
#     #     else:
#     #         # Don't group payments: Create one batch per move.
#     #         if not self.group_payment:
#     #             new_batches = []
#     #             for batch_result in batches:
#     #                 for line in batch_result['lines']:
#     #                     new_batches.append({
#     #                         **batch_result,
#     #                         'lines': line,
#     #                     })
#     #             batches = new_batches
#     #
#     #         for batch_result in batches:
#     #             to_process.append({
#     #                 'create_vals': self._create_payment_vals_from_batch(batch_result),
#     #                 'to_reconcile': batch_result['lines'],
#     #                 'batch': batch_result,
#     #             })
#     #
#     #     payments = self._init_payments(to_process, edit_mode=edit_mode)
#     #     self._post_payments(to_process, edit_mode=edit_mode)
#     #     self._reconcile_payments(to_process, edit_mode=edit_mode)
#     #     return payments

    def _post_payments(self, to_process, edit_mode=False):
        """ Post the newly created payments.

        :param to_process:  A list of python dictionary, one for each payment to create, containing:
                            * create_vals:  The values used for the 'create' method.
                            * to_reconcile: The journal items to perform the reconciliation.
                            * batch:        A python dict containing everything you want about the source journal items
                                            to which a payment will be created (see '_get_batches').
        :param edit_mode:   Is the wizard in edition mode.
        """
        payments = self.env['account.payment']
        for vals in to_process:
            payments |= vals['payment']
        payments.button_approved()
#
#     def _reconcile_payments(self, to_process, edit_mode=False):
#         """ Reconcile the payments.
#
#         :param to_process:  A list of python dictionary, one for each payment to create, containing:
#                             * create_vals:  The values used for the 'create' method.
#                             * to_reconcile: The journal items to perform the reconciliation.
#                             * batch:        A python dict containing everything you want about the source journal items
#                                             to which a payment will be created (see '_get_batches').
#         :param edit_mode:   Is the wizard in edition mode.
#         """
#         domain = [('account_internal_type', 'in', ('receivable', 'payable')), ('reconciled', '=', False)]
#         for vals in to_process:
#             payment_lines = vals['payment'].line_ids.filtered_domain(domain)
#             lines = vals['to_reconcile']
#
#             for account in payment_lines.account_id:
#                 (payment_lines + lines)\
#                     .filtered_domain([('account_id', '=', account.id), ('reconciled', '=', False)])\
#                     .reconcile()
#
class AccountMoveLineInh(models.Model):
    _inherit = "account.move.line"

    def reconcile(self):
        ''' Reconcile the current move lines all together.
        :return: A dictionary representing a summary of what has been done during the reconciliation:
                * partials:             A recorset of all account.partial.reconcile created during the reconciliation.
                * full_reconcile:       An account.full.reconcile record created when there is nothing left to reconcile
                                        in the involved lines.
                * tax_cash_basis_moves: An account.move recordset representing the tax cash basis journal entries.
        '''
        results = {}

        if not self:
            return results

        # List unpaid invoices
        not_paid_invoices = self.move_id.filtered(
            lambda move: move.is_invoice(include_receipts=True) and move.payment_state not in ('paid', 'in_payment')
        )

        # ==== Check the lines can be reconciled together ====
        company = None
        account = None
        for line in self:
            if line.reconciled:
                raise UserError(_("You are trying to reconcile some entries that are already reconciled."))
            if not line.account_id.reconcile and line.account_id.internal_type != 'liquidity':
                raise UserError(
                    _("Account %s does not allow reconciliation. First change the configuration of this account to allow it.")
                    % line.account_id.display_name)
            # if line.move_id.state != 'posted':
            #     raise UserError(_('You can only reconcile posted entries.'))
            if company is None:
                company = line.company_id
            elif line.company_id != company:
                raise UserError(_("Entries doesn't belong to the same company: %s != %s")
                                % (company.display_name, line.company_id.display_name))
            if account is None:
                account = line.account_id
            elif line.account_id != account:
                raise UserError(_("Entries are not from the same account: %s != %s")
                                % (account.display_name, line.account_id.display_name))

        sorted_lines = self.sorted(key=lambda line: (line.date_maturity or line.date, line.currency_id))

        # ==== Collect all involved lines through the existing reconciliation ====

        involved_lines = sorted_lines
        involved_partials = self.env['account.partial.reconcile']
        current_lines = involved_lines
        current_partials = involved_partials
        while current_lines:
            current_partials = (current_lines.matched_debit_ids + current_lines.matched_credit_ids) - current_partials
            involved_partials += current_partials
            current_lines = (current_partials.debit_move_id + current_partials.credit_move_id) - current_lines
            involved_lines += current_lines

        # ==== Create partials ====

        partials = self.env['account.partial.reconcile'].create(sorted_lines._prepare_reconciliation_partials())

        # Track newly created partials.
        results['partials'] = partials
        involved_partials += partials

        # ==== Create entries for cash basis taxes ====

        is_cash_basis_needed = account.user_type_id.type in ('receivable', 'payable')
        if is_cash_basis_needed and not self._context.get('move_reverse_cancel'):
            tax_cash_basis_moves = partials._create_tax_cash_basis_moves()
            results['tax_cash_basis_moves'] = tax_cash_basis_moves

        # ==== Check if a full reconcile is needed ====

        if involved_lines[0].currency_id and all(
                line.currency_id == involved_lines[0].currency_id for line in involved_lines):
            is_full_needed = all(line.currency_id.is_zero(line.amount_residual_currency) for line in involved_lines)
        else:
            is_full_needed = all(line.company_currency_id.is_zero(line.amount_residual) for line in involved_lines)

        if is_full_needed:

            # ==== Create the exchange difference move ====

            if self._context.get('no_exchange_difference'):
                exchange_move = None
            else:
                exchange_move = involved_lines._create_exchange_difference_move()
                if exchange_move:
                    exchange_move_lines = exchange_move.line_ids.filtered(lambda line: line.account_id == account)

                    # Track newly created lines.
                    involved_lines += exchange_move_lines

                    # Track newly created partials.
                    exchange_diff_partials = exchange_move_lines.matched_debit_ids \
                                             + exchange_move_lines.matched_credit_ids
                    involved_partials += exchange_diff_partials
                    results['partials'] += exchange_diff_partials

                    exchange_move._post(soft=False)

            # ==== Create the full reconcile ====

            results['full_reconcile'] = self.env['account.full.reconcile'].create({
                'exchange_move_id': exchange_move and exchange_move.id,
                'partial_reconcile_ids': [(6, 0, involved_partials.ids)],
                'reconciled_line_ids': [(6, 0, involved_lines.ids)],
            })

        # Trigger action for paid invoices
        not_paid_invoices \
            .filtered(lambda move: move.payment_state in ('paid', 'in_payment')) \
            .action_invoice_paid()

        return results