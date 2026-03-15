
    -- user table
    create table user(
    id int primary key auto_increment,
    email varchar(20) unique not null,
    password varchar(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    amount bigint DEFAULT 0
    account number bigint
    ) 
-- transactions table
create table transactions(
    sender_email varchar(55) unique,
    Receiver_email varchar(55) unique,
    amount_transfered bigint,
    amount_type varchar(55),
    transaction_purpose varchar(255)
    transaction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)