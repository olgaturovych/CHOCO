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
        ship_form_email.send_keys('fitotest1111@ukr.net')


        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='firstname']")
        ship_form_first_name.click()
        ship_form_first_name.send_keys("Test")
        ship_form_first_name = self.driver.find_element(By.XPATH, "//input[@name='lastname']")
        ship_form_first_name.send_keys('Testing')
        ship_form_street = self.driver.find_element(By.XPATH, "//input[@name='street[0]']")
        ship_form_street.send_keys('Mattenstrasse 107')
        ship_form_post_code = self.driver.find_element(By.XPATH, "//input[@name='postcode']")
        ship_form_post_code.send_keys('2345')
        city_field = self.driver.find_element(By.XPATH, "//input[@name='city']")
        city_field.send_keys('Praz-jean')
        ship_form_phone = self.driver.find_element(By.XPATH, "//input[@name='telephone']")
        ship_form_phone.send_keys('+410627347093')

        proceed_to_payment_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Proceed to Payment')]")
        proceed_to_payment_button.click()
        


    def test_payment_success(self):
        twint_payment = self.driver.find_element(By.XPATH, '//input[@type="radio" and @name="payment[method]" and @class="radio" and @id="adyen_twint" and @value="adyen_twint"]')
        twint_payment.click()
        terms_agree = self.driver.find_element(By.ID, 'agreement_twint_4')
        self.driver.execute_script("arguments[0].click();", terms_agree)

        #terms_agree = self.driver.find_element(By.ID, 'agreement_twint_4')
        #terms_agree.click()
        place_order_button = self.driver.find_element(By.XPATH, "//form[contains(@id, 'payment_form_adyen_hpp_twint')]//button[contains(@title, 'Place Order')]")
        #place_order_button.click()
        self.driver.execute_script("arguments[0].click();", place_order_button)

    def test_twint_window(self):
        twint_authorized = self.driver.find_element(By.XPATH, "//button[@value='authorised']")
        twint_authorized.click()
        #twint_success_page = self.driver.find_element(By.XPATH, "//h2[contains(text(), 'Your payment is authorised')]")
        #assert twint_success_page
        #continue_button = self.driver.find_element(By.ID, "//input[contains(@value, 'Continue')]")
        #continue_button.click()
        continue_shopping_button = self.driver.find_element(By.XPATH, "//a//span[contains(text(), 'Continue Shopping')]")
        assert continue_shopping_button






    def teardown_class(self):
        self.driver.quit()

if __name__ == "__main__":
    pytest.main()
                                   
                                                    
                                                    







""""
    def test_login_with_selenium(self):
        sign_in_button = self.driver.find_element(
            By.XPATH, "//button[text()='Sign In']"
        )
        sign_in_button.click()
        email_field = self.driver.find_element(By.ID, "signinEmail")
        password_field = self.driver.find_element(By.ID, "signinPassword")

        email_field.send_keys(self.user_email)
        password_field.send_keys(self.user_password)
        self.driver.find_element(By.XPATH, "//button[text()='Login']").click()

        assert self.driver.find_element(
            By.XPATH, "//p[contains(text(), 'any cars in your garage')]"
        )

    def test_add_car(self):
        self.driver.find_element(
            By.XPATH, '//button[@class="btn btn-primary" and text()="Add car"]'
        ).click()
        self.driver.find_element(By.ID, "addCarBrand").click()
        self.driver.find_element(
            By.XPATH, '//select[@name="carBrandId"]/option[text()="BMW"]'
        ).click()
        self.driver.find_element(By.ID, "addCarModel").click()
        self.driver.find_element(
            By.XPATH, '//select[@name="carModelId"]/option[text()="X5"]'
        ).click()
        self.driver.find_element(By.ID, "addCarMileage").send_keys("100")
        self.driver.find_element(By.XPATH, '//button[text()="Add"]').click()

    def test_added_car(self):
        assert len(self.driver.find_elements(
            By.XPATH, '//ul//li[@class="car-item"]')
        ) > 0
        
    def test_check_car_api(self):
        expected_brand = "BMW"
        expected_model = "X5"
        expected_mileage = 100

        response = self.session.get(url="https://qauto2.forstudy.space/api/cars")
        assert response.status_code == 200

        cars = response.json()
        # print(cars)
        for car in cars['data']:
            if car['brand'] == expected_brand \
                and car['model'] == expected_model \
                and car['mileage'] == expected_mileage:
                    break
        else:
            raise AssertionError("Car not found in API response")
        
        assert True

    def teardown_class(self):
        self.session.delete(url="https://qauto2.forstudy.space/api/users")
        self.driver.close()

        """