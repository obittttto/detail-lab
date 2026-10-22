from datetime import date

from django import forms

from services.models import Service
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "service",
            "client_name",
            "phone",
            "car",
            "preferred_date",
            "comment",
        ]

        widgets = {
            "service": forms.Select(
                attrs={"class": "form-control"}
            ),
            "client_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Как к вам обращаться",
                    "autocomplete": "name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+375 XX XXX-XX-XX",
                    "type": "tel",
                    "autocomplete": "tel",
                }
            ),
            "car": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Например, BMW 3 Series",
                }
            ),
            "preferred_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Расскажи о состоянии автомобиля",
                    "rows": "3",
                }
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["service"].queryset = (
            Service.objects.filter(is_active=True)
        )

        self.fields["service"].empty_label = "Выберите услугу"
        self.fields["preferred_date"].required = False
        self.fields["comment"].required = False

    def clean_client_name(self):
        name = self.cleaned_data["client_name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Укажите имя длиной не менее двух символов."
            )
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(
            character for character in phone
            if character.isdigit()
        )

        if len(digits) < 9 or len(digits) > 15:
            raise forms.ValidationError(
                "Проверте номер телефона."
            )

        return phone

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get(
            "preferred_date",
        )

        if preferred_date and preferred_date < date.today():
            raise forms.ValidationError(
                "Выберите сегодняшнюю или будущую дату."
            )

        return preferred_date
