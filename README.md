# Mediawiki-automation

  Функции, которые выполняет этот скрипт:
  
  - В выгрузке есть сотрудник, который отсутствует на странице отдела в вики. Нужно добавить этого сотрудника в таблицу со списком действующих сотрудников на странице в вики. 
  - В выгрузке нет сотрудника, который присутствует на странице отдела в вики. Нужно переместить запись об этом сотруднике на странице в вики из таблицы действующих сотрудников отдела в таблицу бывших сотрудников. 
  - Сотрудник есть и в выгрузке, и на странице отдела в вики, однако значение полей "должность" или "пометки отдела кадров" отличаются. Нужно обновить соответствующие поля в вики, т.к. информация в выгрузке более актуальна. 
  - Ситуация перехода сотрудника из одного отдела в другой равносильна выполнению сценариев 1 и 2 одновременно, поскольку для старого отдела сотрудник в выгрузке будет отсутствовать, а для нового он появится. Отдельно учитывать этот случай не нужно, код должен его корректно обрабатывать за счет сценариев 1 и 2. 
  - В выгрузке присутствует отдел, страницы которого нет в вики. Нужно создать новую страницу для этого отдела, на странице создать таблицу текущих сотрудников на основе данных из выгрузки, и пустую таблицу бывших сотрудников (только заголовки столбцов).

  Для поиска таблиц среди разметки медиавики у таблиц присутствует `id` (у таблицы действующих сотрудников `id = addTable`, для уволенных `id = fireTable`)

  Пример кода вики:

`
<strong>Таблица действующих сотрудников</strong>
{| id = addtable class="wikitable"
|-
!| Отдел
!|Подразделение
!| ФИО
!| Должность
!| Доп. Информация
|-
|}

<strong>Таблица уволенных сотрудников</strong>

{| id = firetable class="wikitable"
|-
!| Отдел
!| Подразделение
!| ФИО
!| Должность
!| Доп. Информация
|-
|}
`
