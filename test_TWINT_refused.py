import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestCheckoutWithTWINT:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1440, 900)
        self.driver.get('https://stage.laderach.com/ch-en')
        self.driver.implicitly_wait(20)

    def test_handle_popup(self):
        accept_all_button = self.driver.find_element(By.XPATH, '//div[(@aria-label="menu")]//button[contains(text(), "Accept all")]')
        accept_all_button.click()


    def test_add_to_cart(self):
        all_products_cat = self.driver.find_element(By.XPATH, "//a[contains(@class, 'pagebuilder-button-primary') and @href='https://stage.laderach.com/ch-en/alle-produkte']")
        all_products_cat.click()
        
        expected_url = 'https://stage.laderach.com/ch-en/alle-produkte'
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))

        current_url = self.driver.current_url 
        assert current_url == expected_url

        open_product = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Chocolate Heart Gianduja Milk gold 32g')]")
        open_product.click()
        add_to_cart = self.driver.find_element(By.ID, 'product-addtocart-button')
        add_to_cart.click()
        added_product_success = self.driver.find_element(By.XPATH, "//div[contains(@class, 'success')]")
        assert added_product_success

    def test_cart_page(self):
        add_to_cart = self.driver.find_element(By.ID, 'product-addtocart-button')
        add_to_cart.click()
        open_cart = self.driver.find_element(By.XPATH, "//a[contains(@href, 'https://stage.laderach.com/ch-en/checkout/cart/')]")
        open_cart.click()
        proceed_to_checkout = self.driver.find_element(By.XPATH, "//button[contains(@class, 'proceed-to-checkout-button')]")
        proceed_to_checkout.click()
        ship_form_email = self.driver.find_element(By.ID, "customer-email")
        ship_form_email.send_keys('fitotest1@ukr.net')


        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='firstname']")
        ship_form_first_name.click()
        ship_form_first_name.send_keys('Test')
        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='lastname']")
        ship_form_first_name.send_keys("Testing")
        ship_form_street = self.driver.find_element(By.XPATH, "//input[@name='street[0]']")
        ship_form_street.send_keys('Mattenstrasse 107')
        ship_form_post_code = self.driver.find_element(By.XPATH, "//input[@name='postcode']")
        ship_form_post_code.send_keys('5643')
        city_field = self.driver.find_element(By.XPATH, "//input[@name='city']")
        city_field.send_keys('Praz-jean')
        ship_form_phone = self.driver.find_element(By.XPATH, "//input[@name='telephone']")
        ship_form_phone.send_keys('+410627347093')

        proceed_to_payment_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Payment')]")
        proceed_to_payment_button.click()
        


    def test_payment_cancelled(self):
        twint_payment = self.driver.find_element(By.XPATH, '//input[@type="radio" and @name="payment[method]" and @class="radio" and @id="adyen_twint" and @value="adyen_twint"]')
        twint_payment.click()
        terms_agree = self.driver.find_element(By.ID, 'agreement_twint_4')
        self.driver.execute_script("arguments[0].click();", terms_agree)

        place_order_button = self.driver.find_element(By.XPATH, "//form[contains(@id, 'payment_form_adyen_hpp_twint')]//button[contains(@title, 'Place Order')]")
        self.driver.execute_script("arguments[0].click();", place_order_button)

    def test_twint_window(self):
        twint_error = self.driver.find_element(By.XPATH, "//button[@value='refused']")
        twint_error.click()
        error_message = self.driver.find_element(By.XPATH, "//div[contains(@data-ui-id, 'checkout-cart-validationmessages-message-error')]")
        assert error_message
        expected_url = f'https://stage.laderach.com/ch-en/checkout/cart/?utm_nooverride=1'
        assert self.driver.current_url == expected_url




    def teardown_class(self):
        self.driver.quit()

if __name__ == "__main__":
    pytest.main()
                                   
                                                    
                                                    




