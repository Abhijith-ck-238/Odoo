"""model for wizard"""
import openpyxl
import base64
from io import BytesIO
from odoo import Command
from odoo.exceptions import UserError
from odoo import fields, models


class FileWizard(models.TransientModel):
    """class or import line wizard"""
    _name = "file.wizard"
    _description = "This is the model for the new wizard"

    fil = fields.Binary(string="Upload File")

    def action_import_lines(self):
        """import the products in the uploaded xls file
        to the current sale order"""
        try:

            sale_order_id = self.env.context.get('active_id')
            sale_order = self.env['sale.order'].browse(sale_order_id)
            wb = openpyxl.load_workbook(filename=BytesIO(
                base64.b64decode(self.fil)), read_only=True)
            ws = wb.active
            for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,
                                       max_col=None, values_only=True):
                search_product = self.env['product.template'].search([
                    ('name', '=', record[0])])
                if not search_product:
                    product_created = self.env['product.template'].create({
                        'name': record[0],
                        'uom_id': self.env['uom.uom'].search([
                            ('name', '=', record[1])]).id,
                        'description': record[2],
                        'list_price': record[3]
                    })
                    sale_order_line = (sale_order.order_line.
                                       filtered(lambda line: line.
                                                product_id.name == record[0]))
                    if sale_order_line:
                        sale_order_line.write({
                            'product_uom_qty':
                                sale_order_line.product_uom_qty + record[4]
                        })
                    else:
                        sale_order.update({
                            'order_line': [
                                Command.create({
                                    'product_id': product_created.
                                    product_variant_id.id,
                                    'product_uom_qty': record[4],
                                    'tax_id': False,
                                    'price_unit': record[3]
                                })
                            ]
                        })
                else:
                    sale_order_line = (sale_order.order_line.
                                       filtered(lambda line: line.
                                                product_id.name == record[0]))
                    if sale_order_line:
                        sale_order_line.write({
                            'product_uom_qty':
                                sale_order_line.product_uom_qty + record[4]
                        })
                    else:
                        sale_order.update({
                            'order_line': [
                                Command.create({
                                    'product_id': search_product.
                                    product_variant_id.id,
                                    'tax_id': False,
                                    'product_uom_qty': record[4]
                                })],

                        })
        except:
            raise UserError('Please insert a valid file')
