# Django Serious Shop   <img src="https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg"> <img src="https://img.shields.io/badge/python-3.8-blue.svg"> <img src="https://img.shields.io/badge/License-MIT-yellow.svg">

Django-serious-shop is an e-commerce website project built using the Django framework and a simple front-end (created from scratch). 
> The project is still under development, so far without full functionality implemented (see [Todo list](#todo-list))

## Features
* Using Modified Preorder Tree Traversal for even to easier category managment 
* Customized admin panel to make creating products smoother
* Key company information (e.g. Delivery or About us section) stored in a database (PostgreSQL) for faster changes
* Added WYSIWYM content editor - ckeditor to create better and prettier product descriptions
* Fully support AnonymousUser thanks to sessions
* Suport boths billing and shipping addresses
* Orders can be paid by paying cards
* Email notification are send using asynchronous tasks in order to ensure the best possible user-experience
* Comprehensively covered with tests to make sure everything is working properly

## Todo list
- [ ] add sorting bar
- [ ] create connections between quantity in the warehouse and order
- [ ] handle bank transfers and other paying methods
- [ ] add posibility of creating and managing own profile
- [ ] add historical info
- [ ] add localization and internationalization support 
- [ ] add extra functionality for confirmed users e.g. wish list
- [ ] panel for managing refunds and promo codes
- [ ] and many others

## Small Piece of Work

![web1](https://user-images.githubusercontent.com/58914643/90765939-0fe3ca00-e2eb-11ea-97ce-ab69b74a4a7d.jpg)
___
![web2](https://user-images.githubusercontent.com/58914643/90765943-1114f700-e2eb-11ea-92d1-ffe9ea5bb04e.jpg)
___
![web3](https://user-images.githubusercontent.com/58914643/90765945-11ad8d80-e2eb-11ea-82e6-5ca5b72b17df.jpg)
___

## Developing

### Built With

* [Django](https://github.com/django/django)
* [django-mptt](https://github.com/django-mptt/django-mptt)
* [django-localflavor](https://github.com/django/django-localflavor)
* [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails)
* [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor)
* [django-allauth](https://github.com/pennersr/django-allauth)
* [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
* [Braintree](https://github.com/braintree/braintree_python)

### Clone Project

```
git clone https://github.com/ImustAdmit/django-serious-shop.git
```

## Database

PosgreSQL use as Database.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
