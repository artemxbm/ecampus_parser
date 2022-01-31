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


def connect():
    session = requests.session()
    session.mount('https://', TLSAdapter())
    html_post = session.post("https://api.campus.kpi.ua/oauth/token",
                             data={'username': 'kav1004201', 'password': 'BjVcPEo3', 'grant_type': 'password'})
    _ = session.get("https://ecampus.kpi.ua/home", data=html_post.cookies)
    _ = session.get("https://campus.kpi.ua", data=html_post.cookies)
    return session, html_post


def id_parser():
    session, html_post = connect()
    html_get = session.get("https://campus.kpi.ua/student/index.php?mode=studysheet", data=html_post.cookies)
    parser = BeautifulSoup(html_get.content, "html.parser")
    parser = parser.find("tbody")
    id_subject = {}
    for k in parser.find_all("tr"):
        pos = str(k).find("id=")
        subject_id = (int(str(k)[pos+3:pos+8]))
        pos2 = str(k)[pos + 10:].find(",")
        subject = (str(k)[pos + 10:pos + 10 + pos2])
        id_subject[subject_id] = subject
    return id_subject

def campus_parser():
    session, html_post = connect()
    ids = id_parser()
    with open("pars.txt", "w") as file:
        for ID in ids.keys():
            url = f"https://campus.kpi.ua/student/index.php?mode=studysheet&action=view&id={ID}"
            html_get = session.get(url, data=html_post.cookies)
            parser = BeautifulSoup(html_get.content, "html.parser")
            parser = parser.find("div", id="tabs-0")
            for i in parser.find_all("tbody"):
                # finds all td tags in tr tags
                for k in i.find_all("tr"):
                    # prints all td tags with a text format
                    j = k.find_all("td")
                    file.write(f"{j[0].text} {j[1].text} {j[2].text} {j[3].text}\n")


def main():
    campus_parser()
    with open("pars.txt", 'r') as f:
        print("".join(i for i in f.readlines()))


def debug():
    id_parser()


if __name__ == "__main__":
    main()
