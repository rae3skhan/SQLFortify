import requests
from bs4 import BeautifulSoup


def get_all_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all("form")


def test_sqli(url, data):
    vulnerable = False
    for payload in ['"', "'"]:
        data["username"] = payload
        response = requests.post(url, data=data)
        if payload in response.text:
            vulnerable = True
            print("Potential SQL Injection vulnerability found!")
            break
    return vulnerable


def main():
    target_url = input("Enter the target URL: ")
    forms = get_all_forms(target_url)
    for form in forms:
        form_action = form.get("action")
        form_method = form.get("method")
        form_data = {}
        for input_field in form.find_all("input"):
            input_name = input_field.get("name")
            input_type = input_field.get("type")
            input_value = input_field.get("value", "")
            form_data[input_name] = input_value

        if form_method == "post":
            if test_sqli(target_url + form_action, form_data):
                break  # Stop testing other forms if a vulnerability is found


if __name__ == "__main__":
    main()
