import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestCheckoutWithCreditCard:
    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1440, 900)
        self.driver.get("https://stage.laderach.com/ca-en")
        self.driver.implicitly_wait(20)

    def test_handle_popup(self):
        accept_all_button = self.driver.find_element(By.XPATH, '//div[(@aria-label="menu")]//button[contains(text(), "Accept all")]')
        accept_all_button.click()


    def test_add_to_cart(self):
        all_products_cat = self.driver.find_element(By.XPATH, "//a[contains(@class, 'pagebuilder-button-primary') and @href='https://stage.laderach.com/ca-en/alle-produkte']")
        all_products_cat.click()
        
        # Use an explicit wait to wait for the page to load and the URL to change
        expected_url = 'https://stage.laderach.com/ca-en/alle-produkte'
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))

        current_url = self.driver.current_url 
        assert current_url == expected_url

        open_product = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Chocolate Snack Milk')]")
        open_product.click()
        add_to_cart = self.driver.find_element(By.ID, 'product-addtocart-button')
        add_to_cart.click()
        added_product_success = self.driver.find_element(By.XPATH, "//div[contains(@class, 'success')]")
        assert added_product_success

    def test_cart_page(self):
        add_to_cart = self.driver.find_element(By.ID, 'product-addtocart-button')
        add_to_cart.click()
        open_cart = self.driver.find_element(By.XPATH, "//a[contains(@href, 'https://stage.laderach.com/ca-en/checkout/cart/')]")
        open_cart.click()
        
        proceed_to_checkout = self.driver.find_element(By.XPATH, "//button[contains(@class, 'proceed-to-checkout-button')]")
        #self.driver.execute_script("arguments[0].scrollIntoView();", proceed_to_checkout)
        self.driver.execute_script("arguments[0].click();", proceed_to_checkout)
        ship_form_email = self.driver.find_element(By.ID, "customer-email")
        ship_form_email.send_keys('fitotest1111@ukr.net')


        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='firstname']")
        ship_form_first_name.click()
        ship_form_first_name.send_keys('Test')
        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='lastname']")
        ship_form_first_name.send_keys('Testing')
        ship_form_street = self.driver.find_element(By.XPATH, "//input[@name='street[0]']")
        ship_form_street.send_keys('587 Speers Road')
        ship_form_post_code = self.driver.find_element(By.XPATH, "//input[@name='postcode']")
        ship_form_post_code.send_keys('L6H 3H5')
        city_field = self.driver.find_element(By.XPATH, "//input[@name='city']")
        city_field.send_keys("Oakville")
        province_field = self.driver.find_element(By.XPATH, "//select//option[contains(@data-title, 'Ontario')]")
        province_field.click()
        ship_form_phone = self.driver.find_element(By.XPATH, "//input[@name='telephone']")
        ship_form_phone.send_keys('+410627347093')

        ship_method = self.driver.find_element(By.XPATH, "//input[@type='radio' and @value='ups_02']")
        self.driver.execute_script("arguments[0].scrollIntoView();", ship_method)
        self.driver.execute_script("arguments[0].click();", ship_method)

        proceed_to_payment_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Payment')]")
        #proceed_to_payment_button.click()
        self.driver.execute_script("arguments[0].click();", proceed_to_payment_button)
        


    def test_payment_success(self):
        cc_payment = self.driver.find_element(By.XPATH, '//input[@type="radio" and @name="payment[method]" and @class="radio" and @id="adyen_cc" and @value="adyen_cc"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", cc_payment)
        self.driver.execute_script("arguments[0].click();", cc_payment)

       
        iframe_element1 = self.driver.find_element(By.XPATH, "//iframe[contains(@title, 'Iframe for secured card number')]")
        self.driver.switch_to.frame(iframe_element1)
        card_number_field = self.driver.find_element(By.XPATH, '//input[contains(@data-fieldtype, "encryptedCardNumber")]')
        card_number_field.send_keys('4111111111111111')
        self.driver.switch_to.default_content()
        
        iframe_element2 = self.driver.find_element(By.XPATH, "//iframe[contains(@title, 'Iframe for secured card expiry date')]")
        self.driver.switch_to.frame(iframe_element2)
        card_date_field = self.driver.find_element(By.XPATH, "//input[contains(@aria-label, 'Expiry date')]")
        card_date_field.send_keys('0330')
        self.driver.switch_to.default_content()

        

        iframe_element3 = self.driver.find_element(By.XPATH, "//iframe[contains(@title, 'Iframe for secured card security code')]")
        self.driver.switch_to.frame(iframe_element3)
        card_code = self.driver.find_element(By.XPATH, '//input[contains(@data-fieldtype, "encryptedSecurityCode")]')
        card_code.send_keys(737)
        self.driver.switch_to.default_content()

        terms_agree = self.driver.find_element(By.ID, 'agreement_adyen_cc_1')
        self.driver.execute_script("arguments[0].click();", terms_agree)

        place_order_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'button') and contains(@class, 'primary') and contains(@class, 'checkout') and contains(@title, 'Place Order') and not(@disabled)]")
        place_order_button.click()

        expected_url1 = f'https://stage.laderach.com/ca-en/checkout/onepage/success/'
        WebDriverWait(self.driver, 20).until(EC.url_to_be(expected_url1))
        assert self.driver.current_url == expected_url1







    def teardown_class(self):
        self.driver.quit()

if __name__ == "__main__":
    pytest.main()
                                   
                                                    
                                                    


