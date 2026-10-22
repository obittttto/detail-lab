from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import BookingForm
from .telegram import send_telegram_message, verify_telegram_init_data

@require_http_methods(["GET", "POST"])
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            # Получаем данные, переданные Telegram Web App
            init_data = request.POST.get("telegram_init_data", "")

            # Проверяем подлинность данных на сервере
            telegram_id = verify_telegram_init_data(init_data)

            if telegram_id is not None:
                booking.telegram_user_id = telegram_id

            booking.save()

            text = (
                "🔔 НОВАЯ ЗАЯВКА — DETAIL LAB\n\n"
                f"👤 Клиент: {booking.client_name}\n"
                f"📞 Телефон: {booking.phone}\n"
                f"🚘 Автомобиль: {booking.car}\n"
                f"🧽 Услуга: {booking.service.title}\n"
                f"📅 Желаемая дата: "
                f"{booking.preferred_date or 'Не указана'}\n"
                f"💬 Комментарий: "
                f"{booking.comment or 'Нет'}\n"
                f"🆔 Номер заявки: {booking.pk}"
            )

            send_telegram_message(text)

            messages.success(
                request,
                "Заявка принята! Мы свяжемся с вами"
                "для подтверждения записи."
            )

            return redirect(
                f"/booking/success/?id={booking.pk}"
            )

    else:
        form = BookingForm(
            initial={
                "service": request.GET.get("service")
            }
        )
    return render(
        request,
        "booking.html",
        {"form": form},
    )

def booking_success(request):
    return render(
        request,
        "booking_success.html",
    )


# Create your views here.
