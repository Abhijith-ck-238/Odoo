# Part of Odoo. See LICENSE file for full copyright and licensing details.

from unittest.mock import patch

from werkzeug.exceptions import Forbidden

from odoo.tests import tagged
from odoo.tools import mute_logger

from odoo.addons.payment_multisafepay.controllers.main import MultiSafePayController
from odoo.addons.payment_aps.tests.common import APSCommon


@tagged('post_install', '-at_install')
class TestProcessingFlows(APSCommon):

    @mute_logger('odoo.addons.payment_aps.controllers.main')
    def test_redirect_notification_triggers_processing(self):
        """ Test that receiving a redirect notification triggers the processing of the notification
        data. """
        self._create_transaction(flow='redirect')
        url = self._build_url(MultiSafePayController._return_url)
        with patch(
            'odoo.addons.payment_multisafepay.controllers.main.MultiSafePayController._verify_notification_signature'
        ), patch(
            'odoo.addons.payment.models.payment_transaction.PaymentTransaction'
            '._handle_notification_data'
        ) as handle_notification_data_mock:
            self._make_http_post_request(url, data=self.notification_data)
            self.assertEqual(handle_notification_data_mock.call_count, 1)

