from django.db import models
import datetime
from ian_account.managers import SoftDeleteManager, GetAllObjects
from ian_account.models import UserSettings



class BaseTransaction(models.Model):

    id = models.BigAutoField(primary_key=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("ian_account.User", on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey("ian_account.Organization", on_delete=models.CASCADE)
    amount = models.FloatField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = SoftDeleteManager()
    all_objects = GetAllObjects()

    def soft_delete(self):
        self.deleted_at = datetime.datetime.utcnow()
        self.is_active = False
        self.save()

class Transaction(BaseTransaction):

    """
    Tracks all transactions in a specified organization
    """

    DEPOSIT = "DE"
    WITHDRAW = "WI"

    TRANSACTION_TYPE = [
        (DEPOSIT, "Deposit"),
        (WITHDRAW, "Withdraw"),
    ]

    PENDING = "pending"
    SUCCESSFUL = "successful"
    CANCELED = "canceled"
    FAILED = "failed"
    TRANSACTION_STATUS = [
        (PENDING, "pending"),
        (SUCCESSFUL, "successful"),
        (CANCELED, "canceled"),
        (FAILED, "failed"),
    ]

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, default=DEPOSIT)
    recipient = models.ForeignKey("ian_account.User", related_name='recepient', on_delete=models.CASCADE, null=True)
    transaction_status = models.CharField( max_length=20, choices=TRANSACTION_STATUS, default=PENDING)
    metadata = models.JSONField(default=dict)

    @property
    def wallet_balance(self):
        balance = 0
        user_setting: UserSettings.objects.all().last()
        transactions: Transaction = Transaction.objects.filter(transaction_status=self.SUCCESSFUL, organization=user_setting.organization)
        for transaction in transactions:
            if transaction.transaction_type == self.DEPOSIT:
                balance += transaction.amount
            else:
                balance -= transaction.amount

        return balance

    class Meta:
        ordering = ("-timestamp",)


class Request(models.Model):

    """
    Tracks all Requests in a specified organization
    """

    PRE_PAYMENT = "pre_payment"
    REIMBURSEMENT = "reimbursement"

    REQUEST_TYPE = [
        (PRE_PAYMENT, "pre_payment"),
        (REIMBURSEMENT, "reimbursement"),
    ]

    PENDING = "pending"
    REJECTED = "rejected"
    APPROVED = "approved"
    PAID_SUCCESSFUL = "paid_successful"


    REQUEST_STATUS = [
        (PENDING, "pending"),
        (REJECTED, "rejected"),
        (APPROVED, "approved"),
        (PAID_SUCCESSFUL, "paid_successful"),
    ]

    id = models.BigAutoField(primary_key=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey("ian_account.User", on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey("ian_account.Organization", on_delete=models.CASCADE)
    amount = models.FloatField()
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE, default=REQUEST_TYPE)
    request_status = models.CharField(max_length=20, choices=REQUEST_STATUS, default=PRE_PAYMENT)
    purpose = models.CharField(max_length=200)
    transaction = models.ForeignKey("Transaction", on_delete=models.CASCADE, related_name="request_transaction", null=True)
    file = models.FileField(upload_to='receipts', null=True)

    objects = SoftDeleteManager()
    all_objects = GetAllObjects()


    class Meta:
        ordering = ("-timestamp",)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.utcnow()
        self.is_active = False
        self.save()




