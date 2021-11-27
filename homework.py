class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        text_info0 = f'Тип тренировки: {self.training_type}; '
        text_info1 = f'Длительность: {self.duration:.3f} ч.; '
        text_info2 = f'Дистанция: {self.distance:.3f} км; '
        text_info3 = f'Ср. скорость: {self.speed:.3f} км/ч; '
        text_info4 = f'Потрачено ккал: {self.calories:.3f}.'
        return text_info0 + text_info1 + text_info2 + text_info3 + text_info4


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        massage_obj: InfoMessage = InfoMessage(
            self.__class__.__name__,
            duration,
            distance,
            speed,
            calories
        )
        return massage_obj


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        coef_cal1: int = 18
        coef_cal2: int = 20
        time = self.duration * 60
        mean_speed: float = self.get_mean_speed()
        return (coef_cal1 * mean_speed -
                coef_cal2) * self.weight / Training.M_IN_KM * time


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(
                self,
                action: int,
                duration: float,
                weight: float,
                height: float
    ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coef_walk1: float = 0.035
        coef_walk2: float = 0.029
        mean_speed: float = self.get_mean_speed()
        time = self.duration * 60
        return (coef_walk1 * self.weight + (mean_speed ** 2 // self.height) *
                coef_walk2 * self.weight) * time


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        distance: float = self.length_pool * self.count_pool / Training.M_IN_KM
        return distance / self.duration

    def get_spent_calories(self) -> float:
        coef_cal = 1.1
        return (self.get_mean_speed() + coef_cal) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    code_training = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type in code_training.keys():
        return code_training[workout_type](*data)
    else:
        return ""


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
