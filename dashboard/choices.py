PROVINCES_CHOICES = [
    ('Mazowieckie', 'Mazowieckie'),
    ('Śląskie', 'Śląskie'),
    ('Wielkopolskie', 'Wielkopolskie'),
    ('Małopolskie', 'Małopolskie'),
    ('Dolnośląskie', 'Dolnośląskie'),
    ('Łódzkie', 'Łódzkie'),
    ('Pomorskie', 'Pomorskie'),
    ('Podkarpackie', 'Podkarpackie'),
    ('Lubelskie', 'Lubelskie'),
    ('Kujawsko-pomorskie', 'Kujawsko-pomorskie'),
    ('Zachodniopomorskie', 'Zachodniopomorskie'),
    ('Warmińsko-mazurskie', 'Warmińsko-mazurskie'),
    ('Świętokrzyskie', 'Świętokrzyskie'),
    ('Podlaskie', 'Podlaskie'),
    ('Lubuskie', 'Lubuskie'),
    ('Opolskie', 'Opolskie'),
]


P24_STATUS_INITIATED = 1
P24_STATUS_FAKE = 2
P24_STATUS_ACCEPTED_VERIFIED = 3
P24_STATUS_ACCEPTED_NOT_VERIFIED = 4
P24_STATUS_REJECTED = 5
P24_STATUS_CHOICES = (
    (P24_STATUS_INITIATED, u'Initiated'),
    (P24_STATUS_FAKE, u'Fake'),  # i.e. not completed POST
    (P24_STATUS_ACCEPTED_VERIFIED, u'Accepted and verified'),
    (P24_STATUS_ACCEPTED_NOT_VERIFIED, u'Accepted, but NOT verified'),
    (P24_STATUS_REJECTED, u'Rejected'),
)