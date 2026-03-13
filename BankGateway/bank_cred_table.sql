CREATE TABLE users (
    Account_number BIGINT PRIMARY KEY NOT NULL,
    Name VARCHAR(25) NOT NULL,
    Caste VARCHAR(25) NOT NULL,
    age INT NOT NULL CHECK (age >= 18),
    Email VARCHAR(30) UNIQUE,
    password VARCHAR(40) NOT NULL,
    city VARCHAR(40) NOT NULL,
    Amount BIGINT NOT NULL
);

-- Insert some dummy data
INSERT INTO users (Account_number, Name, Caste, age, Email, password, city, Amount) VALUES
(1000000001, 'Sujan Thapa', 'Bahun', 25, 'sujan.thapa@gmail.com', 'pass123', 'Kathmandu', 50000),
(1000000002, 'Aarati Rai', 'Rai', 30, 'aarati.rai@gmail.com', 'pass234', 'Pokhara', 75000),
(1000000003, 'Binod Lama', 'Chhetri', 22, 'binod.lama@gmail.com', 'pass345', 'Lalitpur', 60000),
(1000000004, 'Diksha Gurung', 'Gurung', 28, 'diksha.gurung@gmail.com', 'pass456', 'Bhaktapur', 82000),
(1000000005, 'Manoj Magar', 'Magar', 35, 'manoj.magar@gmail.com', 'pass567', 'Dharan', 91000);