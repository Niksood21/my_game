##### Авторы: Никита Родин, Александр Воробьев

# Игра космический шутер

### Наша игра начинается с того, что вы появляетесь на карте и управляете космическим кораблем, главная цель это уничтожить вражеские корабли и выжить самому. Управление космическим кораблем происходит с помощью нажатий на стрелки(вверх, вниз, влево и вправо).

### class "Player" отвечает за существование вашего корабля:

* функция "move_left" отвечает за движение влево
* функция "move_right" отвечает за движение вправо
* функция "move_up" отвечает за движение вперед
* функция "move_down" отвечает за движение вниз
* функция "draw" отображает корабль на экране.
* функция "damage" отвечает за регистрацию урона по космическому кораблю
* функция "draw_health_bar" отвечает за отрисовку полосы здоровья
* функция "restart" отвечает за появление игрок в определенном месте после игрового сеанса
* функция "alive" возвращает состояние игрока (жив/мертв)
* функция "restart_hp" восстанавливает здоровье после игрового сеанса

### class "Enemy" отвечает за существование вражеских кораблей:

* функция "draw" отображает корабль на экране.
* функция "random_move" отвечает за движение противников в случайном направлении
* функция "shoot" создает выстрелы
* функция "update_bullets" удаляет выстрелы, если они вылетели за игровое окно
* функция "damage" отвечает за регистрацию урона по противникам
* функция "alive" проверяет жив ли враг
* функции "get_x", "get_y" возвращают координаты противников
* функция "restart" заставляет противников появиться в случайном месте после игрового сеанса
* фукнция "draw" отрисовывает вражеские пули
* функция "restart_hp" восстанавливает здоровье после игрового сеанса

### class "Boss" отвечает за существование босса

* функция "move" отвечает за движение босса
* функция "damage" отвечает за регистрацию урона по боссу
* функция "shoot" создает выстрелы босса
* функция "alive" проверяет жив ли босс
* функция "draw" отрисовывает пули босса на экране и удаляет их, если они вылетели за экран
* функции "get_x", "get_y" возвращают координаты босса
* функция "restart_hp" восстанавливает здоровье босса после игрового сеанса

### class "Bullet" отвечает за создание выстрела:

* функция "move" отвечает за движение пули
* функция "draw" отвечает за отрисовку пули на экране
* функция "is_off_screen" проверяет вылетела ли пуля за экран.

### class "EnemyBullet" отвечает за создание пуль врагов

* функция "move" отвечает за движение пули
* функция "draw" отрисовывает пулю на экране
* функция "is_off_screen" проверяет, вылетела ли пуля за игровое окно

### class "BossBullet" отвечает за создание пули босса

* функция "move" отвечает за движение пули
* функция "draw" отрисовывает пулю на экране
* функция "is_off_screen" проверяет, вылетела ли пуля за игровое окно

### Функция "initial_window" отвечает за отображение начального текста на экране 