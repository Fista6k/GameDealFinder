from django.core.mail import send_mail
from django.conf import settings

def send_price_email(user, game, price):
    subject = f"Цена на {game.title} упала до нужной отметки"
    message = (
        f"Цена игры {game.title} стала {price}.\n\n"
        f"Проверьте выгодное предложение на сайте.\n\n"
        f"https://game-deal-finder.onrender.com/"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )