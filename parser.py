import requests
from bs4 import BeautifulSoup
import ssl


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


def campus_parser(log, password):
    session = requests.session()
    session.mount('https://', TLSAdapter())
    html_post = session.post("https://api.campus.kpi.ua/oauth/token",
                             data={f'username': {log}, 'password': {password}, 'grant_type': 'password'})
    _ = session.get("https://ecampus.kpi.ua/home", data=html_post.cookies)
    _ = session.get("https://campus.kpi.ua", data=html_post.cookies)
    html_get = session.get("https://campus.kpi.ua/student/index.php?mode=studysheet", data=html_post.cookies)
    parser = BeautifulSoup(html_get.content, "html.parser")
    parser = parser.find("tbody")
    id_subject = {}
    for k in parser.find_all("tr"):
        pos = str(k).find("id=")
        subject_id = (int(str(k)[pos + 3:pos + 8]))
        pos2 = str(k)[pos + 10:].find(",")
        subject = (str(k)[pos + 10:pos + 10 + pos2])
        if subject[-1] == ".":
            subject = subject[:-1]
        id_subject[subject_id] = subject
    data_str = []
    for ID in id_subject.keys():
        url = f"https://campus.kpi.ua/student/index.php?mode=studysheet&action=view&id={ID}"
        html_get = session.get(url, data=html_post.cookies)
        parser = BeautifulSoup(html_get.content, "html.parser")
        parser = parser.find("div", id="tabs-0")
        for i in parser.find_all("tbody"):
            # finds all td tags in tr tags
            for k in i.find_all("tr"):
                # prints all td tags with a text format
                j = k.find_all("td")
                if j[1].text != "":
                    data_str.append([id_subject[ID], j[0].text, j[1].text, j[2].text, j[3].text])
    return data_str


# f"{ids[ID]} {j[0].text} {j[1].text} {j[2].text} {j[3].text}
def main():
    ...
    # with open("pars.txt", 'r') as f:
    # print("".join(i for i in f.readlines()))


def debug():
    ...


if __name__ == "__main__":
    main()
