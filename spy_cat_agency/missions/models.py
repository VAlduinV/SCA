from django.db import models
from cats.models import Cat

# Create your models here.

class Mission(models.Model):
    """
        Модель для представлення місій у системі шпигунського агентства.

        Місія пов'язана з котом, який її виконує, та має статус виконання.

        Атрибути:
            cat (ForeignKey): посилання на модель Cat, яка виконує місію.
                              Може бути порожнім, якщо місія ще не призначена коту.
            is_completed (BooleanField): вказує, чи завершена місія.
                                          За замовчуванням — False.
    """
    cat = models.ForeignKey(Cat, on_delete=models.SET_NULL, null=True, blank=True, related_name="missions")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        """
            Повертає текстове представлення місії.

            Формат:
                "Mission <id> - Completed: <is_completed>"

            Повертає:
                str: Текстове представлення місії.
        """
        return f"Mission {self.id} - Completed: {self.is_completed}"


class Target(models.Model):
    """
        Модель для представлення цілей місії.

        Ціль пов'язана з місією та містить інформацію про:
        - Назву цілі.
        - Країну, де знаходиться ціль.
        - Нотатки, які залишаються під час шпигунства.
        - Статус виконання.

        Атрибути:
            mission (ForeignKey): посилання на модель Mission, до якої належить ціль.
            name (CharField): назва цілі (до 200 символів).
            country (CharField): країна, де знаходиться ціль (до 100 символів).
            notes (TextField): нотатки, які залишають під час шпигунства. Можуть бути порожніми.
            is_completed (BooleanField): вказує, чи завершена ціль. За замовчуванням — False.
    """
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        """
            Повертає текстове представлення цілі.

            Формат:
                "Target <name> (<country>)"

            Повертає:
                str: текстове представлення цілі.
        """
        return f"Target {self.name} ({self.country})"
