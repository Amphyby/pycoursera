from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points,
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Perception": 4,  # восприятие
            "Endurance": 8,  # выносливость
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):

    def __init__(self, hero):
        self.base = hero

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        return self.base.get_negative_effects()

    @abstractmethod
    def get_stats(self):
        pass


class AbstractNegative(AbstractEffect):
    def get_positive_effects(self):
        return self.base.get_positive_effects()

    @abstractmethod
    def get_negative_effects(self):
        pass

    @abstractmethod
    def get_stats(self):
        pass


class Blessing(AbstractPositive):

    def get_positive_effects(self):
        result = self.base.get_positive_effects().copy()
        result.append("Blessing")
        return result

    def get_stats(self):
        result = self.base.get_stats().copy()
        result["Strength"] = result["Strength"] + 2
        result["Perception"] = result["Perception"] + 2
        result["Endurance"] = result["Endurance"] + 2
        result["Charisma"] = result["Charisma"] + 2
        result["Intelligence"] = result["Intelligence"] + 2
        result["Agility"] = result["Agility"] + 2
        result["Luck"] = result["Luck"] + 2
        return result


class Berserk(AbstractPositive):
    def get_positive_effects(self):
        result = self.base.get_positive_effects().copy()
        result.append("Berserk")
        return result

    def get_stats(self):
        result = self.base.get_stats().copy()
        result["Strength"] = result["Strength"] + 7
        result["Endurance"] = result["Endurance"] + 7
        result["Agility"] = result["Agility"] + 7
        result["Luck"] = result["Luck"] + 7
        result["Charisma"] = result["Charisma"] - 3
        result["Perception"] = result["Perception"] - 3
        result["Intelligence"] = result["Intelligence"] - 3
        result["HP"] = result["HP"] + 50
        return result


class Weakness(AbstractNegative):

    def get_negative_effects(self):
        result = self.base.get_negative_effects().copy()
        result.append("Weakness")
        return result

    def get_stats(self):
        result = self.base.get_stats().copy()
        result["Strength"] = result["Strength"] - 4
        result["Endurance"] = result["Endurance"] - 4
        result["Agility"] = result["Agility"] - 4
        return result


class EvilEye(AbstractNegative):

    def get_negative_effects(self):
        result = self.base.get_negative_effects().copy()
        result.append("EvilEye")
        return result

    def get_stats(self):
        result = self.base.get_stats().copy()
        result["Luck"] = result["Luck"] - 10
        return result


class Curse(AbstractNegative):

    def get_negative_effects(self):
        result = self.base.get_negative_effects().copy()
        result.append("Curse")
        return result

    def get_stats(self):
        result = self.base.get_stats().copy()
        result["Strength"] = result["Strength"] - 2
        result["Perception"] = result["Perception"] - 2
        result["Endurance"] = result["Endurance"] - 2
        result["Charisma"] = result["Charisma"] - 2
        result["Intelligence"] = result["Intelligence"] - 2
        result["Agility"] = result["Agility"] - 2
        result["Luck"] = result["Luck"] - 2
        return result

def test_stats():
    # создадим героя
    hero = Hero()
    # проверим правильность характеристик по-умолчанию
    assert hero.get_stats() == {'HP': 128,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 15,
                                'Perception': 4,
                                'Endurance': 8,
                                'Charisma': 2,
                                'Intelligence': 3,
                                'Agility': 8,
                                'Luck': 1}
    # проверим список отрицательных эффектов
    assert hero.get_negative_effects() == []
    # проверим список положительных эффектов
    assert hero.get_positive_effects() == []
    # наложим эффект Berserk
    brs1 = Berserk(hero)
    # проверим правильность изменения характеристик
    assert brs1.get_stats() == {'HP': 178,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 22,
                                'Perception': 1,
                                'Endurance': 15,
                                'Charisma': -1,
                                'Intelligence': 0,
                                'Agility': 15,
                                'Luck': 8}
    # проверим неизменность списка отрицательных эффектов
    assert brs1.get_negative_effects() == []
    # проверим, что в список положительных эффектов был добавлен Berserk
    assert brs1.get_positive_effects() == ['Berserk']
    # повторное наложение эффекта Berserk
    brs2 = Berserk(brs1)
    # наложение эффекта Curse
    cur1 = Curse(brs2)
    # проверим правильность изменения характеристик
    assert cur1.get_stats() == {'HP': 228,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 27,
                                'Perception': -4,
                                'Endurance': 20,
                                'Charisma': -6,
                                'Intelligence': -5,
                                'Agility': 20,
                                'Luck': 13}
    # проверим правильность добавления эффектов в список положительных эффектов
    assert cur1.get_positive_effects() == ['Berserk', 'Berserk']
    # проверим правильность добавления эффектов в список отрицательных эффектов
    assert cur1.get_negative_effects() == ['Curse']
    # снятие эффекта Berserk
    cur1.base = brs1
    # проверим правильность изменения характеристик
    assert cur1.get_stats() == {'HP': 178,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 20,
                                'Perception': -1,
                                'Endurance': 13,
                                'Charisma': -3,
                                'Intelligence': -2,
                                'Agility': 13,
                                'Luck': 6}
    # проверим правильность удаления эффектов из списка положительных эффектов
    assert cur1.get_positive_effects() == ['Berserk']
    # проверим правильность эффектов в списке отрицательных эффектов
    assert cur1.get_negative_effects() == ['Curse']
    # проверим незменность характеристик у объекта hero
    assert hero.get_stats() == {'HP': 128,
                                'MP': 42,
                                'SP': 100,
                                'Strength': 15,
                                'Perception': 4,
                                'Endurance': 8,
                                'Charisma': 2,
                                'Intelligence': 3,
                                'Agility': 8,
                                'Luck': 1}
    print('All tests - OK!')

class Light:
    def __init__(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]
        self.lights = []
        self.obstacles = []

    def set_dim(self, dim):
        self.dim = dim
        self.grid = [[0 for i in range(dim[0])] for _ in range(dim[1])]

    def set_lights(self, lights):
        self.lights = lights
        self.generate_lights()

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        self.generate_lights()

    def generate_lights(self):
        return self.grid.copy()


class System:
    def __init__(self):
        self.map = self.grid = [[0 for i in range(30)] for _ in range(20)]
        self.map[5][7] = 1  # Источники света
        self.map[5][2] = -1  # Стены

    def get_lightening(self, light_mapper):
        self.lightmap = light_mapper.lighten(self.map)

class MappingAdapter:
    def __init__(self, adaptee):
        self.li = adaptee

    def lighten(self, grid):
        w = len(grid)
        h = len(grid[0])
        self.li.set_dim((h, w))
        lights = []
        walls = []
        for i in range(0,len(grid)):
            for j in range(0,len(grid[i])):
                if grid[i][j] == 1:
                    lights.append((j,i))
                elif grid[i][j] == -1:
                    walls.append((j,i))
        self.li.set_obstacles(walls)
        self.li.set_lights(lights)
        return self.li.generate_lights()

class Engine:
    pass

class ObservableEngine(Engine):
    def __init__(self):
        self.subscribed = set()
    def subscribe(self, watever):
        self.subscribed.add(watever)
    def unsubscribe(self, watever):
        self.subscribed.remove(watever)
    def notify(self, watever):
        for i in self.subscribed:
            i.update(watever)

class AbstractObserver(ABC):
    @abstractmethod
    def update(self, watever):
        pass

class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, watever):
        self.achievements.add(watever["title"])

class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = []
        self.achievements_s = set()

    def update(self, watever):
        if (not watever["title"] in self.achievements_s):
            self.achievements.append(watever)
            self.achievements_s.add(watever["title"])


if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
