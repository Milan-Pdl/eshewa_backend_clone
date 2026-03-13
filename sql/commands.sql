
    -- user table
    create table user(
    id int primary key auto_increment,
    email varchar(20) unique not null,
    password varchar(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) 
