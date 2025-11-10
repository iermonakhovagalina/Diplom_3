import pytest
import allure
from data.urls import MainUrl, URLS


class TestMainPage:

    @allure.title('Проверка перехода по клику на "Конструктор"')
    def test_click_constructor_opens_main_page(self, main_page):
        main_page.click_constructor()
        current_url = main_page.get_current_url()
        assert current_url == MainUrl.MAIN_URL

    @allure.title('Проверка перехода по клику на "Лента заказов"')
    def test_click_order_feed_opens_feed_page(self, main_page):
        main_page.click_order_feed()
        main_page.wait_for_page_load()
        current_url = main_page.get_current_url()
        expected_url = MainUrl.MAIN_URL + URLS.url_feed
        assert current_url == expected_url

    @allure.title('Проверка если кликнуть на ингредиент, появится всплывающее окно с деталями')
    def test_click_ingredient_opens_modal(self, main_page):
        main_page.click_ingredient()
        assert main_page.is_ingredient_modal_visible(), "Модальное окно не открылось"

    @allure.title('Проверка закрытия всплывающего окна по крестику')
    def test_modal_closes_by_x_button(self, main_page):
        main_page.click_ingredient()
        main_page.close_ingredient_modal()
        assert main_page.is_ingredient_modal_closed(), "Модальное окно не закрылось после клика по крестику"

    @allure.title('Увеличение счетчика ингредиента при перетаскивании его в корзину')
    def test_drag_ingredient_increases_counter(self, main_page):
        initial_counter = main_page.get_ingredient_counter()
        main_page.drag_ingredient_to_constructor()
        new_counter = main_page.get_ingredient_counter()
        assert new_counter > initial_counter, f"Счетчик не увеличился. Было: {initial_counter}, стало: {new_counter}"
