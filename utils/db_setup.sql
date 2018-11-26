create table if not exists Locations
(
  location_id serial,
  gpsx        real,
  gpsy        real,
  primary key (location_id)
);

create table if not exists Addresses
(
  address_code int,
  address      text,
  primary key (address_code),
  foreign key (address_code) references Locations (location_id)
    on delete cascade
);

CREATE TABLE IF NOT EXISTS Customers
(
  account_id       serial,
  account_username text,
  customer_name    text,
  customer_surname text,
  email            text,
  location         int,
  phone_number     text,
  primary key (account_id),
  foreign key (location) references Locations (location_id)
    on delete set null
);

create table if not exists Plugs
(
  plug_serial serial,
  primary key (plug_serial)
);

create table if not exists Cars
(
  car_id              serial,
  registration_number text,
  car_model           text,
  car_color           text,
  location            int,
  charge_level        int,
  damage_level        int,
  plug_type           int,
  primary key (car_id),
  foreign key (location) references Locations (location_id)
    on delete set null,
  foreign key (plug_type) references Plugs (plug_serial)
    on delete cascade
);

create table if not exists Charging_stations
(
  charging_station_id serial,
  location            int,
  charging_cost       real,
  primary key (charging_station_id),
  foreign key (location) references Locations (location_id)
    on delete set null
);

create table if not exists Details
(
  detail_serial serial,
  detail_name   text,
  detail_cost   real,
  primary key (detail_serial)
);

create table if not exists Workshops
(
  workshop_id serial,
  location    int,
  primary key (workshop_id),
  foreign key (location) references Locations (location_id)
    on delete set null
);

create table if not exists Detail_provider
(
  provider_id serial,
  name        text,
  surname     text,
  phone       text,
  email       text,
  address     int,
  primary key (provider_id),
  foreign key (address) references Addresses (address_code)
    on delete set null
);

create table if not exists Orders
(
  order_id      serial,
  departure     int,
  destination   int,
  selected_car  int,
  creation_time timestamp,
  end_time      timestamp,
  customer      int,
  distance      real,
  primary key (order_id),
  foreign key (departure) references Locations (location_id)
    on delete set null,
  foreign key (destination) references Locations (location_id)
    on delete set null,
  foreign key (customer) references Customers (account_id)
    on delete cascade
);

create table if not exists Payments
(
  payment_id serial,
  amount     real,
  date       timestamp,
  source     int,
  from_order int,
  primary key (payment_id),
  foreign key (source) references Customers (account_id)
    on delete cascade,
  foreign key (from_order) references Orders(order_id)
    on delete SET NULL
);

create table if not exists Station_plugs
(
  station   int,
  plug      int,
  available int,
  max       int,
  date timestamp,
  primary key (station, plug, date),
  foreign key (station) references Charging_stations (charging_station_id)
    on delete cascade,
  foreign key (plug) references Plugs (plug_serial)
    on delete cascade
);

create table if not exists Workshop_details
(
  workshop int,
  detail   int,
  provider int,
  car int,
  date timestamp,
  primary key (workshop, detail, provider, car, date),
  foreign key (workshop) references Workshops (workshop_id) on delete cascade,
  foreign key (detail) references Details (detail_serial) on delete cascade,
  foreign key (provider) references Detail_provider (provider_id) on delete set null,
  foreign key (car) references Cars(car_id) on delete cascade
);

insert into Plugs(plug_serial) VALUES (DEFAULT);
insert into Plugs(plug_serial) VALUES (DEFAULT);
insert into Plugs(plug_serial) VALUES (DEFAULT);
insert into Plugs(plug_serial) VALUES (DEFAULT);

insert into Details(detail_name, detail_cost) VALUES ('Rumpel', 12);
insert into Details(detail_name, detail_cost) VALUES ('Junk', 100);
insert into Details(detail_name, detail_cost) VALUES ('Coat', 13);
insert into Details(detail_name, detail_cost) VALUES ('Wheel', 57);
insert into Details(detail_name, detail_cost) VALUES ('Axis', 150);
insert into Details(detail_name, detail_cost) VALUES ('Glass', 98);
insert into Details(detail_name, detail_cost) VALUES ('Bumper', 45);
insert into Details(detail_name, detail_cost) VALUES ('Windshield', 103);
insert into Details(detail_name, detail_cost) VALUES ('Mirrors', 10);