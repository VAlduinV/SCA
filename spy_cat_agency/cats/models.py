from django.db import models

# Create your models here.


class Cat(models.Model):
    """
        Модель для представлення котів у системі шпигунського агентства.

        Ця модель описує основні атрибути котів, які працюють у системі:
        - Ім'я кота.
        - Роки досвіду у шпигунстві.
        - Порода кота.
        - Заробітна плата.

        Атрибути:
            name (CharField): ім'я кота (до 100 символів).
            years_of_experience (PositiveIntegerField): кількість років досвіду.
            breed (CharField): порода кота.
            salary (DecimalField): заробітна плата у вигляді десяткового числа
                                   (максимум 10 цифр, з яких 2 після коми).
    """
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """
            Повертає зручне текстове представлення об'єкта Cat.

            Використовується для відображення імені кота в адміністративній панелі або під час роботи з моделлю.

            Повертає:
                str: Ім'я кота.
        """
        return self.name
