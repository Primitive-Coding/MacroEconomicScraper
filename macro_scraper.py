# Operating system imports
import os
import json
import datetime as dt

# Pandas imports
import pandas as pd
import numpy as np

# Requests imports
import requests

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class MacroScraper:
    wait_time = 5

    def __init__(self, debug: bool = False):
        self.browser = None
        self.chrome_driver_path = self._get_chrome_driver_path()
        self.cpi_url = "https://www.rateinflation.com/inflation-rate/usa-historical-inflation-rate/"
        self.fed_funds_url = "https://fred.stlouisfed.org/series/FEDFUNDS"
        self.t10_t2_url = "https://fred.stlouisfed.org/series/T10Y2Y"
        self.base_export_path = self._get_data_export_path()
        self.cpi_file_path = f"{self.base_export_path}\\MacroData\\CPI\\cpi.csv"
        self.fed_funds_path = (
            f"{self.base_export_path}\\MacroData\\FedFunds\\fed_funds.csv"
        )
        self.t10_t2_notes_path = f"{self.base_export_path}\\MacroData\\Treasury_Yield_Spread_10Y_2Y\\Treasury_Yield_Spread_10Y_2Y.csv"
        # Create folders if they do not exist.
        os.makedirs(f"{self.base_export_path}\\MacroData\\CPI", exist_ok=True)
        os.makedirs(f"{self.base_export_path}\\MacroData\\FedFunds", exist_ok=True)
        os.makedirs(
            f"{self.base_export_path}\\MacroData\\Treasury_Yield_Spread_10Y_2Y",
            exist_ok=True,
        )
        """ --- Chrome driver options ---"""
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-gpu")

        self.debug = debug

    """-----------------------------------"""

    def _get_data_export_path(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        return data["data_export_path"]

    """-----------------------------------"""

    def _get_chrome_driver_path(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        return data["chrome_driver_path"]

    """ ---------------------- Consumer Price Index (CPI) ---------------------- """
    """
    Description: Is a widely used economic indicator that measures changes in the average prices paid by consumers 
                 for a basket of goods and services over time.  The CPI is a key metric for assessing inflation,
                 which is the increase in the general level of prices for goods and services in an economy.            
    """
    """-----------------------------------"""

    def update_cpi(self):
        # Get the cpi data in the form of a dataframe.
        df = self._fetch_cpi_externally()
        df.set_index("Date", inplace=True)
        df.replace("N\\A", np.nan, inplace=True)
        df.dropna(inplace=True)
        df.to_csv(self.cpi_file_path)
        return df

    """-----------------------------------"""

    def get_cpi_source(self) -> str:
        return self.cpi_url

    """-----------------------------------"""

    def get_cpi(self):
        try:
            df = pd.read_csv(self.cpi_file_path)
            df.set_index("Date", inplace=True)
            df.replace("N\\A", np.nan, inplace=True)
            df.dropna(inplace=True)
            return df
        except FileNotFoundError:
            df = self.update_cpi()
            return df

    def _fetch_cpi_externally(self):
        """
        Scrape the CPI data from the "CPI url".
        """

        if self.browser == None:
            self.create_browser(url=self.cpi_url)

        # Index should start at 1.
        index = 1

        year_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[1]"
        jan_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[2]"
        feb_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[3]"
        mar_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[4]"
        apr_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[5]"
        may_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[6]"
        jun_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[7]"
        jul_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[8]"
        aug_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[9]"
        sep_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[10]"
        oct_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[11]"
        nov_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[12]"
        dec_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[13]"
        annual_xpath = "/html/body/div/div/div[2]/main/div[3]/table/tbody/tr[{}]/td[14]"

        scraping_cpi = True

        cpi_data = []
        # cpi_dict = {}
        error_count = 0
        error_threshold = 3

        while scraping_cpi:
            try:
                year = self.read_data(xpath=year_xpath.format(index))
                jan_data = self.read_data(xpath=jan_xpath.format(index))
                feb_data = self.read_data(xpath=feb_xpath.format(index))
                mar_data = self.read_data(xpath=mar_xpath.format(index))
                apr_data = self.read_data(xpath=apr_xpath.format(index))
                may_data = self.read_data(xpath=may_xpath.format(index))
                jun_data = self.read_data(xpath=jun_xpath.format(index))
                jul_data = self.read_data(xpath=jul_xpath.format(index))
                aug_data = self.read_data(xpath=aug_xpath.format(index))
                sep_data = self.read_data(xpath=sep_xpath.format(index))
                oct_data = self.read_data(xpath=oct_xpath.format(index))
                nov_data = self.read_data(xpath=nov_xpath.format(index))
                dec_data = self.read_data(xpath=dec_xpath.format(index))
                annual_data = self.read_data(xpath=annual_xpath.format(index))

                # Create a list holding the data.
                data_vars = [
                    jan_data,
                    feb_data,
                    mar_data,
                    apr_data,
                    may_data,
                    jun_data,
                    jul_data,
                    aug_data,
                    sep_data,
                    oct_data,
                    nov_data,
                    dec_data,
                ]

                # Create an empty dictionary to hold the cpi data for the year.
                cpi_dict = {}
                for i in range(len(data_vars)):
                    if data_vars[i].strip() == "":
                        data_vars[i] = "N\A"

                    if "%" in data_vars[i]:
                        data_vars[i] = data_vars[i].replace("%", "")

                    # Assign data to the dictionary
                    month = (
                        len(data_vars) - i
                    )  # Logic to determine the month. The length of "data_vars" should always be 12, so we use i to work down the list. Ex: Iter1: 12 - 0, Iter2: 12-1, Iter3: 12-2. We do this because we want the data to be stored in the dict in reverese.
                    cpi_dict[f"{year}-{month}"] = data_vars[month - 1]
                    if year == "N\\A":
                        scraping_cpi = False

                    if self.debug:
                        print(f"CPI: {cpi_dict}")

            except NoSuchElementException:
                error_count += 1

            if error_count == error_threshold:
                scraping_cpi = False
            cpi_data.append(cpi_dict)
            index += 1
        # Create a DataFrame
        cpi_df = pd.DataFrame(
            [(k, v) for d in cpi_data for k, v in d.items()],
            columns=["Date", "Value"],
        )

        self.clean_close()
        return cpi_df

    """ ---------------------- Fed Funds ---------------------- """
    """
    Description: The federal funds rate is the interest rate at which depository institutions (like banks and credit unions)
                 lend reserve balances to other depository institutions overnight on an uncollateralized basis.
                  In the United States, this rate is determined by the Federal Reserve, which is the country's central bank.
    """
    """-----------------------------------"""

    def update_fed_funds(self):
        df = self._fetch_fed_funds_externally()
        df.set_index("Date", inplace=True)
        df.to_csv(self.fed_funds_path)
        return df

    """-----------------------------------"""

    def get_fed_funds_source(self) -> str:
        return self.fed_funds_url

    """-----------------------------------"""

    def get_fed_funds(self):
        try:
            df = pd.read_csv(self.fed_funds_path)
            df.set_index("Date", inplace=True)
            return df
        except FileNotFoundError:
            df = self.update_fed_funds()
            return df

    """-----------------------------------"""

    def _fetch_fed_funds_externally(self):

        now = dt.datetime.now()
        month = now.month
        year = now.year
        end_date = f"{year}-{month}-1"

        # "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1319&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FEDFUNDS&scale=left&cosd=1954-07-01&coed=2024-05-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-06-27&revision_date=2024-06-27&nd=1954-07-01"
        csv_file_link = f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1319&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=FEDFUNDS&scale=left&cosd=1954-07-01&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-10-05&revision_date=2023-10-05&nd=1954-07-01"
        csv_data = requests.get(csv_file_link)

        # Decode to a string.
        csv_content = csv_data.content.decode("utf-8").split("\n")

        prev_year = None

        data_collected = []
        yearly_data = {}

        for c in csv_content:
            if c == "DATE,FEDFUNDS" or c == "":
                pass
            else:
                try:
                    date, value = c.split(",")
                    year, month, day = date.split("-")
                    formatted_date = f"{year}-{int(month)}"
                    data_collected.append((formatted_date, float(value)))
                # Occurs when trying to split blank value.
                except ValueError:
                    pass

        df = pd.DataFrame(data_collected, columns=["Date", "Value"])
        # Convert rate column to properly display the rate. Previously {:,2f} would be displayed. Still haven't figured out why.
        df["Value"] = df["Value"].apply(lambda x: f"{x:.2f}")
        # Reverse the rows so the newest entries are on top.
        df = df[::-1]
        df.reset_index(drop=True, inplace=True)
        return df

    """-----------------------------------"""

    def clean_CPI_data(self):
        df = pd.read_csv(self.cpi_file_path)
        df["Value"] = df["Value"].str.rstrip("%")
        df["Value"] = pd.to_numeric(df["Value"])
        df = df.dropna()
        df.to_csv(self.cpi_file_path, index=False)

    """ ---------------------- 10-Year Treasury minus 2-Year Treasury ---------------------- """
    """
    Description: Subtracting the 2-Year Treasury yield from the 10-Year Treasury yield, will give you information on the current standing of the yield curve. 
                 When the resulting difference is positive, it means yields for long-duration treasury notes are greater than yields for short-duration treasury notes.
                 When the difference is negative, it means the yields for short-duration treasury notes are greater than yields on long-duration treasury notes. In other words, an inverted yield curve.
                 """
    """-----------------------------------"""

    def update_treasury_yield_spread(self):
        df = self._fetch_treasury_yield_spread_externally()
        df.set_index("Date", inplace=True)
        df.to_csv(self.t10_t2_notes_path)
        return df

    """-----------------------------------"""

    def get_treasury_yield_spread(self) -> pd.DataFrame:

        try:
            df = pd.read_csv(self.t10_t2_notes_path)
            df.set_index("Date", inplace=True)
            return df
        except FileNotFoundError:
            df = self.update_treasury_yield_spread()
            return df

    """-----------------------------------"""

    def _fetch_treasury_yield_spread_externally(self) -> pd.DataFrame:
        now = dt.datetime.now()
        month = now.month
        year = now.year
        end_date = f"{year}-{month}-1"
        csv_file_link = f"https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=T10Y2YM&scale=left&cosd=1976-06-01&coed={end_date}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2023-10-14&revision_date=2023-10-14&nd=1976-06-01"
        csv_data = requests.get(csv_file_link)

        # Decode to a string.
        csv_content = csv_data.content.decode("utf-8").split("\n")
        prev_year = None

        data_collected = []
        yearly_data = {}

        for c in csv_content:
            if c == "DATE,T10Y2Y" or c == "":
                pass
            else:
                try:
                    date, value = c.split(",")
                    year, month, day = date.split("-")
                    formatted_date = f"{year}-{int(month)}"
                    data_collected.append((formatted_date, float(value)))
                # Occurs when trying to split blank value.
                except ValueError:
                    pass

        df = pd.DataFrame(data_collected, columns=["Date", "Value"])
        # Convert rate column to properly display the rate. Previously {:,2f} would be displayed. Still haven't figured out why.
        df["Value"] = df["Value"].apply(lambda x: f"{x:.2f}")
        # Reverse the rows so the newest entries are on top.
        df = df[::-1]
        df.reset_index(drop=True, inplace=True)
        return df

    """-----------------------------------"""

    def get_treasury_yield_source(self) -> str:
        return self.t10_t2_url

    """----------------------------------- Browser Utilities -----------------------------------"""
    """-----------------------------------"""

    """-----------------------------------"""

    def build_snapshot_url(self, year, month, day):
        # Build the date url
        date = self.format_date(year, month, day)

        snapshot_url = self.histroical_url.format(date)
        return snapshot_url

    """-----------------------------------"""

    def create_element(self, xpath: str) -> webdriver.remote.webelement.WebElement:
        """
        :param  xpath: The xpath to the element that we are creating.
        """
        element = self.browser.find_element("xpath", xpath)
        return element

    """-----------------------------------"""
    """-----------------------------------"""
    """-----------------------------------"""
    """-----------------------------------"""
    """-----------------------------------"""
    """-----------------------------------"""

    def create_browser(self, url=None):
        """
        :param url: The website to visit.
        :return: None
        """
        service = Service(executable_path=self.chrome_driver_path)
        self.browser = webdriver.Chrome(service=service, options=self.chrome_options)
        # Default browser route
        if url == None:
            self.browser.get(url=self.sec_annual_url)
        # External browser route
        else:
            self.browser.get(url=url)

    def clean_close(self) -> None:
        self.browser.close()
        self.browser.quit()

    def read_data(
        self, xpath: str, wait: bool = False, _wait_time: int = 5, tag: str = ""
    ) -> str:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: (str) Text of the element.
        """

        if wait:
            try:
                data = (
                    WebDriverWait(self.browser, _wait_time)
                    .until(EC.presence_of_element_located((By.XPATH, xpath)))
                    .text
                )
            except TimeoutException:
                print(f"[Failed Xpath] {xpath}")
                if tag != "":
                    print(f"[Tag]: {tag}")
                raise NoSuchElementException("Element not found")
            except NoSuchElementException:
                print(f"[Failed Xpath] {xpath}")
                return "N\A"
        else:
            try:
                data = self.browser.find_element("xpath", xpath).text
            except NoSuchElementException:
                data = "N\A"
        # Return the text of the element found.
        return data


if __name__ == "__main__":

    m = MacroScraper(debug=True)

    df = m.get_treasury_yield_spread()
    print(f"DF: {df}")
    """
    Logic Here
    """
