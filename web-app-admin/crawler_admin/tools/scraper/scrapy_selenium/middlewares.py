"""This module contains the ``SeleniumMiddleware`` scrapy middleware"""
import time

from importlib import import_module

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait

from .http import SeleniumRequest


class SeleniumMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(
        self,
        driver_name,
        driver_executable_path,
        driver_arguments,
        browser_executable_path,
    ):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        driver_arguments: list
            A list of arguments to initialize the driver
        browser_executable_path: str
            The path of the executable binary of the browser
        """  
        webdriver_base_path = f"selenium.webdriver.{driver_name}"

        driver_klass_module = import_module(f"{webdriver_base_path}.webdriver")
        driver_klass = getattr(driver_klass_module, "WebDriver")
        driver_options_module = import_module(f"{webdriver_base_path}.options")
        driver_options_klass = getattr(driver_options_module, "Options")
 
        driver_options = driver_options_klass()
        print('browser_executable_path',browser_executable_path)
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        for argument in driver_arguments:
            driver_options.add_argument(argument)
        driver_kwargs = {
            "executable_path": driver_executable_path,
            "options": driver_options,
        }

        print('driver_kwargs', driver_kwargs)
        self.driver = driver_klass(**driver_kwargs)

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        driver_name = crawler.settings.get("SELENIUM_DRIVER_NAME")
        driver_executable_path = crawler.settings.get("SELENIUM_DRIVER_EXECUTABLE_PATH")
        browser_executable_path = crawler.settings.get(
            "SELENIUM_BROWSER_EXECUTABLE_PATH"
        )
        driver_arguments = crawler.settings.get("SELENIUM_DRIVER_ARGUMENTS")

        if not driver_name or not driver_executable_path:
            raise NotConfigured(
                "SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set"
            )

        middleware = cls(
            driver_name=driver_name,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
            browser_executable_path=browser_executable_path,
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        """Process a request using the selenium driver if applicable"""

        print("process_request", request)
        if not isinstance(request, SeleniumRequest):
            return None
 
        self.driver.get(request.url)

        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie({"name": cookie_name, "value": cookie_value})

        print(request.wait_loaded)
        if request.wait_loaded:
            time.sleep(request.wait_loaded)
            
        if request.is_scroll_to_end_page:
            loaded = ""
            while loaded != "complete":
                loaded = self.driver.execute_script("return document.readyState;")
                print("loaded", loaded)
                time.sleep(1)

            script_scroll_end_page = """                
                const smoothScroll = async (h) => {
                    let i = h || 0;
                    if (i < document.body.scrollHeight) {
                        setTimeout(() => {
                        window.scrollTo(0, i);
                            smoothScroll(i + document.body.scrollHeight * 0.005);
                        }, 10);
                    }
                }
                smoothScroll()
                //window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
            """
            self.driver.execute_script(script_scroll_end_page)

        if request.wait_until:
            WebDriverWait(self.driver, request.wait_time)

        if request.is_scroll_to_end_page and request.wait_loaded:
            time.sleep(request.wait_loaded)

        if request.screenshot:
            request.meta["screenshot"] = self.driver.get_screenshot_as_png()

        if request.script:
            self.driver.execute_script(request.script)

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({"driver": self.driver})
        
        return HtmlResponse(
            self.driver.current_url, body=body, encoding="utf-8", request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        self.driver.quit()
