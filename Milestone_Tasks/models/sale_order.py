"""inherit sale order and add action to the button that created"""
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    milestone = fields.Integer(string="Mile stone")
    project_count = fields.Integer("project_count",
                                   compute="compute_project_count")

    def compute_project_count(self):
        """check if the project is created or not. to hide the buttons"""
        for pc in self:
            pc.project_count = len(pc.sudo().project_id)

    def action_project_creation(self):
        """create project with same name as sale order name and
        create task as same name as milestone and
        create subtask as same name as product name
        if only one product with same milestone don't create milestone as task,
        instead create task as product name"""
        for record in self:

            projects = self.env['project.project'].search([
                ('id', '=', record.project_id.id)
            ])
            if not projects:
                # CREATE PROJECT
                created_project = record.env['project.project'].create({
                    'name': record.name,
                    'allow_billable': True,
                    'partner_id': record.partner_id.id,
                    'sale_order_id': record.id
                })
                record.env['project.task.type'].create({
                    'name': 'New',
                    'project_ids': [(fields.Command.link(created_project.id))]
                })
                self.write({
                    'project_id': created_project.id
                })
                for product in record.order_line:
                    # occurrence = 0
                    # check milestone count
                    # for milestone in record.order_line:
                    #     if product.milestone == milestone.milestone:
                    #         occurrence += 1
                    occurrence = (record.order_line.
                                  filtered(lambda line: line.
                                           milestone == product.milestone))
                    m_tasks = product.env['project.task'].search([
                        ('name', '=', "Milestone - " + str(product.milestone)),
                        ('project_id.id', '=', created_project.id)
                    ])
                    print(len(occurrence))
                # IF MILESTONE WITH THAT NAME IN THE SAME PROJECT DOESN'T EXIST
                    if not m_tasks:
                        # IF THE MILESTONE HAS ONLY ONE SUBTASKS
                        if len(occurrence) > 1:
                            # parent task(MILESTONE)
                            created_m_task = record.env['project.task'].create({
                                'name': "Milestone - " + str(product.milestone),
                                'project_id': created_project.id,
                                'sale_order_id': self.sudo().id,
                            })
                            # create child task of above task
                            record.env['project.task'].create({
                                'name': created_m_task.name + " " + product.
                                product_template_id.name,
                                'project_id': created_project.id,
                                'parent_id': created_m_task.id,
                                'sale_order_id': self.sudo().id
                            })
                    # parent task (PRODUCT)
                        else:
                            record.env['project.task'].create({
                                'name': product.product_template_id.name,
                                'project_id': created_project.id,
                                'sale_order_id': self.sudo().id
                            })
                    else:
                        # sub task (PRODUCT) if task
                        record.env['project.task'].create({
                            'name': m_tasks.name + " " + product.
                            product_template_id.name,
                            'project_id': created_project.id,
                            'parent_id': m_tasks.id,
                            'sale_order_id': self.sudo().id
                        })

    def action_project_update(self):
        print("self---", self)
        for order in self:
            tasks = order.env['project.task'].search([
                ('sale_order_id', '=', order.sudo().id)
            ])
            project = order.project_id
            print("tasks---", tasks)
            tasks.unlink()
            for product in order.order_line:
                occurrence = 0
                # check milestone count
                for milestone in order.order_line:
                    if product.milestone == milestone.milestone:
                        occurrence += 1
                m_tasks = product.env['project.task'].search([
                    ('name', '=', "Milestone - " + str(product.milestone)),
                    ('project_id.id', '=', project.id)
                ])
                # IF MILESTONE WITH THAT NAME IN THE SAME PROJECT DOESN'T EXIST
                if not m_tasks:
                    # IF THE MILESTONE HAS ONLY ONE SUBTASKS
                    if occurrence > 1:
                        # parent task(MILESTONE)
                        created_m_task = order.env['project.task'].create({
                            'name': "Milestone - " + str(product.milestone),
                            'project_id': project.id,
                            'sale_order_id': self.sudo().id,
                        })
                        # create child task of above task
                        order.env['project.task'].create({
                            'name': created_m_task.name + " " + product.
                            product_template_id.name,
                            'project_id': project.id,
                            'parent_id': created_m_task.id,
                            'sale_order_id': self.sudo().id
                        })
                    # parent task (PRODUCT)
                    else:
                        order.env['project.task'].create({
                            'name': product.product_template_id.name,
                            'project_id': project.id,
                            'sale_order_id': self.sudo().id
                        })
                else:
                    # sub task (PRODUCT) if task
                    order.env['project.task'].create({
                        'name': m_tasks.name + " " + product.
                        product_template_id.name,
                        'project_id': project.id,
                        'parent_id': m_tasks.id,
                        'sale_order_id': self.sudo().id
                    })

