import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

 

class TestCheckoutWithPayPal:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1440, 900)
        self.driver.get("https://stage.laderach.com/ch-en")
        self.driver.implicitly_wait(20)

    def test_handle_popup(self):
        accept_all_button = self.driver.find_element(By.XPATH, '//div[(@aria-label="menu")]//button[contains(text(), "Accept all")]')
        accept_all_button.click()


    def test_add_to_cart(self):
        all_products_cat = self.driver.find_element(By.XPATH, "//a[contains(@class, 'pagebuilder-button-primary') and @href='https://stage.laderach.com/ch-en/alle-produkte']")
        all_products_cat.click()
        
        # Use an explicit wait to wait for the page to load and the URL to change
        expected_url1 = 'https://stage.laderach.com/ch-en/alle-produkte'
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url1))

        current_url = self.driver.current_url 
        assert current_url == expected_url1

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
        ship_form_email.send_keys('fitotest1111@ukr.net')


        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='firstname']")
        ship_form_first_name.click()
        ship_form_first_name.send_keys('Olga')
        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='lastname']")
        ship_form_first_name.send_keys('Testing')
        ship_form_street = self.driver.find_element(By.XPATH, "//input[@name='street[0]']")
        ship_form_street.send_keys('Mattenstrasse 107')
        ship_form_post_code = self.driver.find_element(By.XPATH, "//input[@name='postcode']")
        ship_form_post_code.send_keys('5643')
        city_field = self.driver.find_element(By.XPATH, "//input[@name='city']")
        city_field.send_keys("Praz-jean")
        ship_form_phone = self.driver.find_element(By.XPATH, "//input[@name='telephone']")
        ship_form_phone.send_keys('+410627347093')

        proceed_to_payment_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Payment')]")
        proceed_to_payment_button.click()
        


    def test_payment_success(self):
        pp_payment = self.driver.find_element(By.XPATH, '//input[@type="radio" and @name="payment[method]" and @class="radio" and @id="adyen_paypal" and @value="adyen_paypal"]')
        pp_payment.click()
        terms_agree = self.driver.find_element(By.ID, 'agreement_paypal_4')
        self.driver.execute_script("arguments[0].click();", terms_agree)

    
        iframe_locator = (By.XPATH, "//iframe[contains(@title, 'PayPal')]")
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.frame_to_be_available_and_switch_to_it(iframe_locator))
        paypal_button = self.driver.find_element(By.XPATH, "//div[@role='link'][contains(@class, 'paypal-button')]")
        self.driver.execute_script("arguments[0].click();", paypal_button)
        self.driver.switch_to.default_content()

        popup_window_handle = None
        main_window_handle = self.driver.window_handles[0]

        for window_handle in self.driver.window_handles:
            if window_handle != main_window_handle:
                self.driver.switch_to.window(window_handle)
                popup_window_handle = window_handle
                break

        #opened popup window
        pp_header = self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Pay with PayPal')]")
        assert pp_header
        pp_email = self.driver.find_element(By.XPATH, "//input[contains(@id, 'email')]")
        pp_email.clear()
        pp_email.send_keys(PP_EMAIL)

        next_button = self.driver.find_element(By.ID, 'btnNext')
        next_button.click()


        pp_password = self.driver.find_element(By.ID, 'password')
        pp_password.send_keys(PP_PASS)
        login_pp_button = self.driver.find_element(By.ID, 'btnLogin')
        login_pp_button.click()
        pp_complete_payment= self.driver.find_element(By.ID, 'payment-submit-btn')
        pp_complete_payment.click()
        self.driver.switch_to.window(main_window_handle)
        #continue_shopping_button = self.driver.find_element(By.XPATH, "//a//span[contains(text(), 'Continue Shopping')]")
        #assert continue_shopping_button
        expected_url = f'https://stage.laderach.com/ch-en/checkout/onepage/success/'
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
        assert self.driver.current_url == expected_url





    def teardown_class(self):
        self.driver.quit()

if __name__ == "__main__":
    pytest.main()
                                   
                                                    
                                                    



