# General
import os

CLIENT_ID = os.getenv('CLIENT_ID', '123')

NEQUI_SERVICE_REGION_DEFAULT = 'C001'
NEQUI_SERVICE_REGION = os.getenv('NEQUI_SERVICE_REGION', NEQUI_SERVICE_REGION_DEFAULT)

NEQUI_CHANNEL_REPORTS = os.getenv('NEQUI_CHANNEL_REPORTS', 'MF-001')
NEQUI_CHANNEL_DEPOSIT_WITHDRAWALS = os.getenv('NEQUI_CHANNEL_DEPOSIT_WITHDRAWALS', 'MF-001')
NEQUI_CHANNEL_QR_PAYMENTS = os.getenv('NEQUI_CHANNEL_QR_PAYMENTS', 'PQR03-C001')
NEQUI_CHANNEL_PUSH_PAYMENTS = os.getenv('NEQUI_CHANNEL_PUSH_PAYMENTS', 'PNP04-C001')
NEQUI_CHANNEL_SUBSCRIPTIONS_PAYMENTS = os.getenv('NEQUI_CHANNEL_SUBSCRIPTIONS_PAYMENTS', 'PDA05-C001')

# Status Codes
NEQUI_STATUS_CODE_SUCCESS = '0'
NEQUI_STATUS_DESC_SUCCESS = 'SUCCESS'


NEQUI_PAYMENT_STATUS_CODE_PENDING = '33'
NEQUI_PAYMENT_STATUS_DESC_PENDING = 'PENDING'
NEQUI_PAYMENT_STATUS_CODE_SUCCESS = '35'
NEQUI_PAYMENT_STATUS_DESC_SUCCESS = 'SUCCESS'

NEQUI_PAYMENT_STATUS_DESC_UNKNOWN = 'UNKNOWN'
