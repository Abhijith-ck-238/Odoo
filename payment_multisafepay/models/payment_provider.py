import logging
from odoo import fields, models
from multisafepay.client import Client

_logger = logging.getLogger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', "Multifafepay")],
        ondelete={'multisafepay': 'set default'})
    multisafepay_merchant_key = fields.Char(
        string="Merchant Key",
        help="The key solely used to identify the account with multisafepay",
    )
    multisafepay_api_key = fields.Char(string="API Key",
                                       help="The API key of the webservice user",
                                       )
    multisafepay_secret_key = fields.Char(
        string="multisafepay Secret Key",
    )

    def _aps_get_api_url(self, payload):
        if self.state == 'test':
            msp_client = Client()
            msp_client.set_modus('TEST')
            msp_client.set_api_key(self.multisafepay_api_key)
            order = msp_client.order.create(payload)
            url = order.get('data').get('payment_url')
            return url
