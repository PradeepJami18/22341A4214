# HTTP URL Shortener Microservice
## What is this project about?
This is a **URL Shortener Microservice** built using Python and Flask.  
Basically, it helps to convert long URLs into short, easy-to-share links.  
You can also track how many times your short link is clicked, when it was created, and when it expires.  
Everything is logged in a file using a custom logger I made.
---
## Features
- Shorten long URLs quickly.
- Use a custom shortcode if you want, or let the system generate one automatically.
- Default link validity is 30 minutes, but you can change it.
- Redirects from the short URL to the original URL.
- Tracks clicks with:
  - Timestamp of the click
  - Referrer (where the click came from)
  - Location (coarse-grained)
- Handles errors properly:
  - Invalid shortcode → 400
  - Shortcode already exists → 409
  - Non-existent shortcode → 404
  - Expired shortcode → 410
- Logs everything in `app.log`.
---
## How to set it up
1. Clone the repo:
```bash
git clone https://github.com/PradeepJami18/22341A4214.git
cd 22341A4214
