1. Создавать в репозитории файл requirements.txt, держать его в актуальном состоянии
2. Оставлять в репозитории список заданий
3. Корень репозитория - корень проекта

# TODO

1. Добавить просмотры неавторизованнным пользователем (ip, browser)
2. Добавить сортировку по количеству просмотров (по аналогии с наличием комментариев)
3. Убрать дублирование
4. Сделать ветки комментариев
5. Добавить изображения для статей
    * В статье должна быть превью models.ImageFields
    * В статье может быть до 10 (2) других изображений
    * У изображения должно быть поле alt (у каждого свой)
    * В тексте статьи должны быть указаны плейсхолдеры для изображений
    * Если изображений больше чем плейсхолдеров - не сохраняем
    * Если изображений меньше - не сохраняем

# TODO 20.01.23

## Добавление статей
1. Написать функцию добавления статей, функцию проверки данных
2. Подготовить тестовые данные с разными примерами
   * нормальное количество изображений
   * больше предела
   * ноль изображений
   * нормальное количество плейсхолдеров
   * больше
   * меньше
   * плейсхолдер не по порядку
3. Попробовать реализовать проверки с помощью TestCase*
4. Реализовать редактирование статей
5. Перенести модель с адресами в приложение users