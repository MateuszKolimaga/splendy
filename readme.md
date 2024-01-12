<p align="center">
    <img src="client/src/assets/logo-t2.svg" alt="drawing" width="200"/>
</p>
<p align="center">
⭐ <Strong>Personal finances tracking web app</Strong> ⭐
</p>

<p align="center">
A web application ( built with <strong>Django</strong> and <strong>Vue</strong> ) for managing personal expenses and sharing bills with your friends!
</p>


## Table of contents

- [Features](#features)
- [Technologies](#technologies)
- [Setup](#setup)
- [Dashboard Demo](#dashboard-demo)
- [Login Demo](#login-demo)

## Features

#### 🔒 User authentication and authorization (CAPTCHA included)

#### 📈 Tracking your expenses and income with interactive charts and graphs

#### 💸 Group expense tracking -> Easy splitting of group expenses

#### ⏲️ Real-time updates on the expenses within user groups

#### 📧 Integrated with SendGrid, the application efficiently sends verification emails and reminder emails ( mainly about the user debts )

#### 💬 WebSocket-based chat system, enabling real-time communication between users

All features are showcased in the [Demo](#dashboard-demo) section.

## Technologies
<p align="center">
<strong>Django</strong> (4.2),
<strong>Vue</strong> (3.3),
<strong>Postgres</strong>,
<strong>Bootstrap</strong>,
<strong>Vite</strong>,
<strong>Pug</strong>,
<strong>Sendgrid</strong>,
<strong>Docker</strong>.
</p>
<p align="center">
<img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/django-icon.png" alt="drawing" width="50"/>
<img src="https://cdn-icons-png.flaticon.com/512/5968/5968342.png" alt="drawing" width="50">
<img src="https://www.svgrepo.com/show/303460/redis-logo.svg" alt="drawing" width="50">
<img src="https://upload.wikimedia.org/wikipedia/commons/f/f1/Vue.png?20170311074507" alt="drawing" width="48"/>
<img src="https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/bootstrap-5-logo-icon.png" width="55" />
<img src="https://vitejs.dev/logo.svg" width="50">
<img id="pug" src="https://cdn.icon-icons.com/icons2/2107/PNG/512/file_type_pug_icon_130225.png" alt="drawing" width="50" />
<img src="https://static-00.iconduck.com/assets.00/sendgrid-icon-2048x2048-coy0ar5a.png" alt="drawing" width="40"/>
</p>
<p align="center">
<img src="https://seeklogo.com/images/D/docker-logo-6D6F987702-seeklogo.com.png" alt="drawing" width="55" style="margin-top: 1rem;"/>
</p>


## Setup 
Populate `.env.templates` in `/src` and `/client` and run (in the root directory):

```
docker-compose up
```

Next you can go to `backend` container:

```
docker-compose exec backend sh
```

Create your `superuser`:
```
python manage.py createsuperuser
```

And that's all! Now you can log in to the application under localhost.

__Notice:__  The application containerized in this way is used for development purposes, I have not included the configuration of `nginx`, `daphne` and `gunicorn`.

## Dashboard demo
- __Personal finance__ dashboard: 0:00 - 0:25
- __Expense Sharing__ dashboard: 0:25 - end



https://github.com/MateuszKolimaga/splendy/assets/51016521/0a61db99-5f29-44c4-88cd-359bbc6cdf91



## Login demo



https://github.com/MateuszKolimaga/splendy/assets/51016521/14092306-f87f-4bc4-8733-574132191f34

