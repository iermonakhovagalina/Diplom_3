from pages.base_page import BasePage
from locators.locators import OrderFeedLocators
import allure


class OrderFeedPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Проверить загрузку страницы ленты заказов')
    def is_order_feed_page_loaded(self):
        return self.is_element_visible(OrderFeedLocators.title_orders_list)

    @allure.step('Получить значение счетчика "Выполнено за все время"')
    def get_total_orders_count(self):
        try:
            counter = self.find_element(OrderFeedLocators.total_orders_counter)
            return int(counter.text) if counter.text else 0
        except:
            return 0

    @allure.step('Получить значение счетчика "Выполнено за сегодня"')
    def get_today_orders_count(self):
        try:
            counter = self.find_element(OrderFeedLocators.dayly_orders_counter)
            return int(counter.text) if counter.text else 0
        except:
            return 0

    @allure.step('Получить список номеров заказов в разделе "В работе"')
    def get_orders_in_progress(self):
        try:
            orders_elements = self.find_elements(OrderFeedLocators.number_order_in_job)
            return [order.text for order in orders_elements if order.text]
        except:
            return []

    @allure.step('Получить форматированный список номеров заказов в разделе "В работе"')
    def get_orders_in_progress_normalized(self):
        try:
            orders_elements = self.find_elements(OrderFeedLocators.number_order_in_job)
            normalized_orders = []
            for order in orders_elements:
                if order.text:
                    normalized_orders.append(str(int(order.text)))
            return normalized_orders
        except:
            return []

    @allure.step('Форматировать номер заказа')
    def normalize_order_number(self, order_number):
        if isinstance(order_number, str):
            return str(int(order_number))
        else:
            return str(order_number)

    @allure.step('Ждать обновления счетчиков')
    def wait_for_counters_update(self, initial_total, initial_today, timeout=15):
        """
        Если initial_total == 0 — игнорируем 'за всё время' и ждём роста 'за сегодня'.
        Если initial_today == 0 — игнорируем 'за сегодня' и ждём роста 'за всё время'.
        Если оба не 0 — ждём роста обоих.
        """
        import time

        watch_total = initial_total != 0
        watch_today = initial_today != 0

        start = time.time()
        while time.time() - start < timeout:
            current_total = self.get_total_orders_count()
            current_today = self.get_today_orders_count()

            if watch_total and watch_today:
                if current_total > initial_total and current_today > initial_today:
                    return True
            elif watch_total:
                if current_total > initial_total:
                    return True
            elif watch_today:
                if current_today > initial_today:
                    return True
            else:
                # Если оба == 0 (теоретически), ждём роста любого
                if current_total > 0 or current_today > 0:
                    return True

            time.sleep(0.5)

        return False

    @allure.step('Ждать появления заказа в разделе "В работе"')
    def wait_for_order_in_progress(self, order_number, timeout=15):
        import time
        normalized_order = self.normalize_order_number(order_number)
        start_time = time.time()

        while time.time() - start_time < timeout:
            orders_in_progress = self.get_orders_in_progress_normalized()
            if normalized_order in orders_in_progress:
                return True
        return False

