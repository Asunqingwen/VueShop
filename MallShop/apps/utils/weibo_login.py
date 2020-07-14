def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = "http://149.129.105.109:8080/complete/weibo/"
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id=2689096765,
                                                                                            redirect_uri=redirect_uri)
    print(auth_url)


def get_access_token(code):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    re_dict = requests.post(access_token_url, data={
        "client_id": 2689096765,
        "client_secret": "fe95738f099d68a0a5b08a8ba9c6bee4",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://149.129.105.109:8080/complete/weibo/",
    })
    print(re_dict.text)


def get_user_info(access_token, uid):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}".format(
        access_token=access_token, uid=uid)
    print(user_url)


if __name__ == '__main__':
    # get_auth_url()
    # get_access_token(code="196624069454bc0e2580f429b183cfcd")
    get_user_info("2.008XQPTBTuKzvC18d34be9cezAfjfC", "1348285073")
