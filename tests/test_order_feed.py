import pytest
import allure

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


class TestOrderFeed:

    @allure.title('При создании нового заказа счётчик "Выполнено за всё время" увеличивается (UI)')
    def test_new_order_increases_total_counter(self, login_user, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        # Открываем сайт и фиксируем исходное значение счётчика
        main_page.open()
        main_page.click_order_feed()
        initial_total = order_feed_page.get_total_orders_count()

        # Создаём заказ целиком через UI
        main_page.click_constructor()
        _ = main_page.create_order_ui()

        # Возвращаемся в ленту и ждём обновления
        main_page.click_order_feed()
        order_feed_page.wait_for_counters_update(initial_total, 0)

        # Один финальный ассерт
        new_total = order_feed_page.get_total_orders_count()
        assert new_total > initial_total, (
            f"'Выполнено за всё время' не увеличился. Было: {initial_total}, стало: {new_total}"
        )

    @allure.title('При создании нового заказа счётчик "Выполнено за сегодня" увеличивается (UI)')
    def test_new_order_increases_today_counter(self, login_user, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        # Открываем сайт и фиксируем исходное значение счётчика
        main_page.open()
        main_page.click_order_feed()
        initial_today = order_feed_page.get_today_orders_count()

        # Создаём заказ целиком через UI
        main_page.click_constructor()
        _ = main_page.create_order_ui()

        # Возвращаемся в ленту и ждём обновления
        main_page.click_order_feed()
        order_feed_page.wait_for_counters_update(0, initial_today)

        # Один финальный ассерт
        new_today = order_feed_page.get_today_orders_count()
        assert new_today > initial_today, (
            f"'Выполнено за сегодня' не увеличился. Было: {initial_today}, стало: {new_today}"
        )

    @allure.title('После оформления заказа его номер появляется в разделе "В работе" (UI)')
    def test_order_number_appears_in_progress(self, login_user, driver):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        # Открываем сайт и переходим в ленту
        main_page.open()
        main_page.click_order_feed()

        # Создаём заказ через UI
        main_page.click_constructor()
        order_number = main_page.create_order_ui()
        normalized = order_feed_page.normalize_order_number(order_number)

        # Проверяем, что номер появился «В работе»
        main_page.click_order_feed()
        order_feed_page.wait_for_order_in_progress(normalized)

        # Один финальный ассерт
        orders_in_progress = order_feed_page.get_orders_in_progress_normalized()
        assert normalized in orders_in_progress, (
            f"Заказ {order_number} не найден в разделе 'В работе'. "
            f"Текущие заказы: {orders_in_progress}"
        )
