# InstaFrame

1:1 your photos for Instagram!

InstaFrame is a micro web-app that transforms your photo to be
of aspect-ratio 1:1 by adding white-bars to either top/bottom or
left/right edges.

## Getting started

You'll need Python 3.10.2, heroku-cli and poetry installed on your system.
Then clone the repo, install the dependencies and start a development server.

```sh
git clone https://github.com/tillhainbach/insta-frame.git
cd insta-frame
poetry install
export QUART_APP="insta_frame:create_app()"
poetry run quart run
```
