import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriver, ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
# Set up Edge options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--headless")

from selenium.webdriver.common.by import By
from datetime import datetime
from datetime import timedelta
import threading
"""from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriver, ChromeDriverManager
from selenium import webdriver

options = Options()
options.add_argument("--start-maximized")

# 1. Get the path to the ChromeDriver executable using ChromeDriverManager
driver_path = ChromeDriverManager().install()


# 3. Pass the Service object to the webdriver.Chrome constructor using the 'service' argument
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# Example of how you might use the driver (e.g., open a website)
driver.get("https://www.google.com")"""
import dateparser

# Export to Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def apply_filter(driver,year, month, day):
    element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'postedAfter'))
        )
    
    post_after = driver.find_element(By.ID,'postedAfter')
    post_after.click()
    time.sleep(1)

    # post_after.send_keys(Keys.CONTROL, "a")
    # post_after.clear()
    post_after.send_keys(year)
    post_after.send_keys(Keys.ARROW_LEFT)
    post_after.send_keys(day)
    post_after.send_keys(Keys.ARROW_LEFT)
    post_after.send_keys(Keys.ARROW_LEFT)
    post_after.send_keys(month)

    question = driver.find_element(By.ID, "threadTypeQuestionsLabel")
    question.click()

    stat = driver.find_element(By.ID,"threadStatusType")
    stats = stat.find_elements(By.CLASS_NAME,"c-checkbox")
    stats[-1].find_element(By.TAG_NAME,"span").click()

    op = driver.find_element(By.ID,"advancedFilterOptionBar")
    ops = op.find_elements(By.CLASS_NAME,'c-label')
    ops[0].find_element(By.TAG_NAME,"span").click()

    apply_button = driver.find_element(By.ID,'applyButton')
    apply_button.click()

def get_thread_link(page_url, driver, year, month, day):
    
    link = []
    driver.get(page_url)
    st.text(page_url)
    time.sleep(10)
    try:
        apply_filter(driver, year, month, day)
    except:
        return link
    try:
        
        while True:
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source)
            threads = soup.find_all("div",class_ ="c-card")
            for i in threads:
                url = i.find('a',class_='c-hyperlink')
                link.append(url['href'])

            try:
                driver.find_element(By.CLASS_NAME,"nextText").click()
            except:
                break
        print(page_url,":",len(link))
        return link
    except:
        print(page_url,":",len(link))
        return link

def get_info(case, driver):
    try:
        driver.get(case)

        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'asking-text-asked-on-link'))
        )
        history_button = driver.find_element(By.CLASS_NAME,'asking-text-asked-on-link')
        history_button.click()

        time.sleep(2)
        soup = BeautifulSoup(driver.page_source)
        x = soup.find('div', class_='rsp-history-table')
        tbody = x.find('tbody')
        row = tbody.find_all('tr')
        created = row[-1].find('td',class_='rsp-history-cell-nowrap').text
        
        # Convert the original datetime string to a datetime object
        datetime_obj = created.replace('\n','').strip()

        # Convert the datetime object to the desired format
        new_datetime_str = datetime_obj


        x = soup.find("ul", id="threadQuestionInfoAppliesToItems")
        y = x.find_all('a')
        tag = []

        for i in y:
            tag.append(i.text)

        category = ' / '.join(tag)
        


        return [category, new_datetime_str]
    except: return ["",""]


def main(root, year, month, day):
    all_data = {}

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    thread_link = []

    thread_link = thread_link+get_thread_link(root,driver, year, month, day)

    for t in thread_link:
        all_data[t] = get_info(t, driver)
    
    return all_data


# Initialize session state
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'elapsed' not in st.session_state:
    st.session_state.elapsed = 0
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

# Timer functions
def start_timer():
    st.session_state.start_time = time.time()
    st.session_state.timer_running = True

def stop_timer():
    st.session_state.timer_running = False
    st.session_state.elapsed = int(time.time() - st.session_state.start_time)



# Initialize session state for historical submissions
if 'submissions' not in st.session_state:
    st.session_state['submissions'] = []

st.sidebar.info("⚠️⚠️⚠️On refresh or page exit, data will not be saved!!!")

# Display historical submissions in sidebar
st.sidebar.markdown("### Historical Submissions")
history_labels = [
    f"{i+1}. {sub['date']} - {sub['region']}" for i, sub in enumerate(st.session_state['submissions'])
]
selected_history = st.sidebar.selectbox("View a previous submission", ["➕ New"] + history_labels)
# --- Main Content ---
st.title("Community Data Scraping 🤖")
st.markdown("### Filtering")

# Date picker
selected_date = st.date_input("📅 Post After", date.today())

# Country and locale mapping
country_locale_map = {
    "🇺🇸 United States": "en-us",
    "🇨🇿 Czech Republic": "cs-cz",
    "🇩🇰 Denmark": "da-dk",
    "🇩🇪 Germany": "de-de",
    "🇪🇸 Spain": "es-es",
    "🇫🇷 France": "fr-fr",
    "🇮🇹 Italy": "it-it",
    "🇭🇺 Hungary": "hu-hu",
    "🇳🇱 Netherlands": "nl-nl",
    "🇳🇴 Norway": "nb-no",
    "🇵🇱 Poland": "pl-pl",
    "🇧🇷 Brazil": "pt-br",
    "🇫🇮 Finland": "fi-fi",
    "🇸🇪 Sweden": "sv-se",
    "🇹🇷 Turkey": "tr-tr",
    "🇬🇷 Greece": "el-gr",
    "🇷🇺 Russia": "ru-ru",
    "🇹🇭 Thailand": "th-th",
    "🇰🇷 South Korea": "ko-kr",
    "🇨🇳 China (Simplified)": "zh-hans",
    "🇨🇳 China (Traditional)": "zh-hant",
    "🇯🇵 Japan": "ja-jp",
    "🇸🇦 Saudi Arabia": "ar-sa",
    "🇮🇱 Israel": "he-il"
}

# Region selection
locale_code = st.multiselect("🌏Select a region (site)", ["🌐ALL"]+list(country_locale_map.keys()))
if "🌐ALL" in locale_code:
    selected_sites = [country_locale_map[i] for i in list(country_locale_map.keys())]
else:
    selected_sites = [country_locale_map[i] for i in locale_code]

# Root URLs
root_urls = {
    "Teams for Business":"https://answers.microsoft.com/{}/msteams/forum/msteams_TfB",
    "Teams for Education":"https://answers.microsoft.com/{}/msteams/forum/msteams_TfE",
    "Office for Business":"https://answers.microsoft.com/{}/msoffice/forum/msoffice_OfB",
    "Office for Education":"https://answers.microsoft.com/{}/msoffice/forum/msoffice_OfE",
    "Outlook":"https://answers.microsoft.com/{}/outlook_com/forum"
}

root = st.multiselect("🖥️Select a root URL", ["🗃️ALL"]+list(root_urls.keys()))
if "🗃️ALL" in root:
    selected_roots = [root_urls[i] for i in list(root_urls.keys())]
else:
    selected_roots = [root_urls[i] for i in root]

# Construct full URL

import itertools
combinations = list(itertools.product(selected_sites, selected_roots))

full_url =  [j.format(i) for i,j in combinations]
st.info(str(len(full_url))+" url(s) are selected")

# Button to trigger crawling and save submission
if st.button("Start Crawling"):
    st.info("Launching Selenium crawler...")
    start_timer()

    year = selected_date.year
    month = selected_date.month
    day = selected_date.day
    output_data = []
    


    for r in full_url:
        st.markdown("###Progess")
        output_data.append(main(r,year, month, day))

        st.info(str(len(output_data[-1]))+ " records found")
    # Placeholder for Selenium logic
    st.success("Crawling completed (placeholder).")

    urls = []
    tags = []
    created_date = []

    for i in output_data:
        for j,k in i.items():
            urls.append(j)
            tags.append(k[0])
            created_date.append(dateparser.parse(k[1]).strftime("%Y-%m-%d") if dateparser.parse(k[1]) else k[1])

    df = pd.DataFrame({"url":urls,"tag":tags,"Created_datetime":created_date})
    
    stop_timer()
    st.success(f"Crawling completed in {st.session_state.elapsed} seconds.")
    # st.info(output_data)
    # df = df.T
    # df.columns = ["Tag","Created Date"]
    # df.reset_index(inplace=True, names="url")

    # Display DataFrame
    st.markdown("###Output Data")
    st.dataframe(df)

    excel_data = convert_df_to_excel(df)

    st.download_button(
        label="📥 Export as Excel",
        data=excel_data,
        file_name="sample_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Save submission to session state
    st.session_state['submissions'].append({
        "date": selected_date,
        "region": "1",
        "url": full_url,
        "data": df,
        "export_data": excel_data
    })

# Display selected historical submission
if selected_history and selected_history in history_labels:
    index = history_labels.index(selected_history)
    selected_submission = st.session_state['submissions'][index]

    st.markdown("###📜Historical Submission")
    st.write(f"**Date:** {selected_submission['date']}")
    st.write(f"**Region:** {selected_submission['region']}")
    st.write(f"**URL:** link")

    st.dataframe(selected_submission['data'])

    st.download_button(
        label="📥 Export as Excel",
        data=selected_submission['export_data'],
        file_name="sample_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: right;'>"
    "<span style='font-size: 24px;'></span>"
    "</div>",
    unsafe_allow_html=True
)
st.caption("Made with Streamlit")
