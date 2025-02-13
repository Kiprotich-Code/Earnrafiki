from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import CustomUser
from .models import Account

@receiver(post_save, sender=Account)
def handle_referral_reward(sender, instance, created, **kwargs):
    """ This signal is triggered after an account's balance is updated or created.
        It checks if the account is eligible for referral reward. """
    if created or instance.balance > 0:  # Trigger reward if the account balance is updated
        if instance.is_eligible_for_reward():
            referrer_account = instance.referred_by.account
            # Check if the referrer hasn't received the reward yet
            if not referrer_account.referral_reward_received:
                # Give $100 to the referrer (you can change this to any amount you wish)
                referrer_account.balance += 100.00
                referrer_account.referral_reward_received = True  # Mark as rewarded
                referrer_account.save()
                # Optionally, you can also mark the referred account as eligible for a reward
                instance.referral_reward_received = True
                instance.save()