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
- [X] add sorting bar
- [X] create connections between quantity in the warehouse and order
- [ ] handle bank transfers and other paying methods
- [ ] add posibility of creating and managing own profile
- [ ] add historical info
- [ ] add localization and internationalization support 
- [ ] add extra functionality for confirmed users e.g. wish list
- [ ] panel for managing refunds and promo codes
- [ ] allow customers to track the package
- [ ] add the ability to generate PDF invoices
- [ ] and many others :alien:

## Small Piece of Work

Main Page         |  Product Details | Cart | Payment
:-------------------------:|:-------------------------:|:-------------------------:|:-------------------------:
![Main Page](https://user-images.githubusercontent.com/58914643/97262214-b8009c80-1820-11eb-9389-4914ad296647.jpg) |![Detail Page](https://user-images.githubusercontent.com/58914643/97262707-bb485800-1821-11eb-9522-bc7c741ebb18.jpg) |![Detail Page](https://user-images.githubusercontent.com/58914643/97262868-0c584c00-1822-11eb-8c05-ef60c00acd10.jpg) |![Main Page](https://user-images.githubusercontent.com/58914643/97262427-19287000-1821-11eb-8f88-6c9a8a6ef69c.jpg)


## Developing

### Built With

* [Django](https://github.com/django/django)
* [django-mptt](https://github.com/django-mptt/django-mptt)
* [django-localflavor](https://github.com/django/django-localflavor)
* [easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails)
* [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor)
* [django-allauth](https://github.com/pennersr/django-allauth)
* [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
* [django-filter](https://github.com/carltongibson/django-filter)
* [celery](https://github.com/celery/celery)
* [Braintree](https://github.com/braintree/braintree_python)

### Clone Project

```
git clone https://github.com/ImustAdmit/django-serious-shop.git
```

## Database

PosgreSQL use as Database.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
