# SSR Connection Test

## Intro

In order to manage all my SSR proxy server, this project is designed for testing all the server in one commands.

## Todo

~~- [ ] insert SSR account~~

~~- [ ] use subscribe url to get ssr proxy information~~

~~- [ ] use g-static to test proxy connection~~

- [x] test proxy automatically

~~- [ ] record proxy status and make a form monthly~~

- [ ] use Telegram Bot to send proxy information

---

now using [SSRSpeed](https://github.com/NyanChanMeow/SSRSpeed) as testing core

- [x] initialize config locally to avoid privacy problem.

- [x] use scheduler to test url automatically

~~- [ ] add ss/ssr switch function~~

- [x] send result to server

## Usage

```bash
git clone https://github.com/Avimitin/SSRCONNTest.git

pip3 install -r requirement.txt

python ./main.py
```

## Alert

This project may occupy ssr link count. Some proxy service provider may not allow too many connection count.