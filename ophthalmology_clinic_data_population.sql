USE OpthalmologyClinicDatabase;
GO

CREATE TABLE [Patient](
    [patient_id] INT IDENTITY(1,1) NOT NULL,
    [name] CHAR(100) NOT NULL,
    [gender] CHAR(10) NOT NULL,
    [date_of_birth] DATE NOT NULL,
    [email] CHAR(150) NOT NULL,
    [phonenumber] INT NOT NULL,
    [password] INT NOT NULL,
    PRIMARY KEY CLUSTERED ([patient_id] ASC)
);
GO

CREATE TABLE [Ophthalmologist](
    [ophthalmologist_id] INT IDENTITY(1,1) NOT NULL,
    [name] CHAR(100) NOT NULL,
    [email] CHAR(150) NOT NULL,
    [phonenumber] INT NOT NULL,
    [clinicname] VARCHAR(150) NOT NULL,
    [clinicaddress] VARCHAR(255) NOT NULL,
    [password] INT NOT NULL,
    PRIMARY KEY CLUSTERED ([ophthalmologist_id] ASC)
);
GO

CREATE TABLE [Appointment](
    [appointment_id] INT IDENTITY(1,1) NOT NULL,
    [patient_id] INT NOT NULL,
    [ophthalmologist_id] INT NOT NULL,
    [appointment_date] DATE NOT NULL,
    [appointment_time] DATETIME NOT NULL,
    [appointment_status] BIT NOT NULL,
    PRIMARY KEY CLUSTERED ([appointment_id] ASC),
    FOREIGN KEY ([patient_id]) REFERENCES [Patient]([patient_id]),
    FOREIGN KEY ([ophthalmologist_id]) REFERENCES
[Ophthalmologist]([ophthalmologist_id])
);
GO

CREATE TABLE [Patient_Record](
    [record_id] INT IDENTITY(1,1) NOT NULL,
    [patient_id] INT NOT NULL,
    [ophthalmologist_id] INT NOT NULL,
    [appointment_id] INT NOT NULL,
    [record_date] DATE NOT NULL,
    [diagnosis] CHAR(255),
    [prescription] CHAR(255),
    [treatment_details] TEXT NOT NULL,
    PRIMARY KEY CLUSTERED ([record_id] ASC),
    FOREIGN KEY ([patient_id]) REFERENCES [Patient]([patient_id]),
    FOREIGN KEY ([ophthalmologist_id]) REFERENCES
[Ophthalmologist]([ophthalmologist_id]),
    FOREIGN KEY ([appointment_id]) REFERENCES [Appointment]([appointment_id])
);
GO


CREATE TABLE [Bill](
    [bill_id] INT IDENTITY(1,1) NOT NULL,
    [patient_id] INT NOT NULL,
    [appointment_id] INT NOT NULL,
    [amount] DECIMAL(10,2) NOT NULL,
    [payment_status] BIT NOT NULL,
    [payment_date] DATE NOT NULL,
    PRIMARY KEY CLUSTERED ([bill_id] ASC),
    FOREIGN KEY ([patient_id]) REFERENCES [Patient]([patient_id]),
    FOREIGN KEY ([appointment_id]) REFERENCES [Appointment]([appointment_id])
);
GO

CREATE TABLE [Feedback](
    [feedback_id] INT IDENTITY(1,1) NOT NULL,
    [patient_id] INT NOT NULL,
    [ophthalmologist_id] INT NOT NULL,
    [rating] INT NOT NULL,
    [comments] TEXT NOT NULL,
    [feedback_date] DATE NOT NULL,
    PRIMARY KEY CLUSTERED ([feedback_id] ASC),
    FOREIGN KEY ([patient_id]) REFERENCES [Patient]([patient_id]),
    FOREIGN KEY ([ophthalmologist_id]) REFERENCES
[Ophthalmologist]([ophthalmologist_id])
);
GO


CREATE TABLE [Notification](
    [notification_id] INT IDENTITY(1,1) NOT NULL,
    [appointment_id] INT NOT NULL,
    [recipient_id] INT NOT NULL,
    [recipient_type] CHAR(20) NOT NULL,
    [sent_date] DATE NOT NULL,
    [message] CHAR(255) NOT NULL,
    [message_read] BIT NOT NULL,
    PRIMARY KEY CLUSTERED ([notification_id] ASC),
    FOREIGN KEY ([appointment_id]) REFERENCES [Appointment]([appointment_id])
);
GO


INSERT INTO [Patient] (name, gender, date_of_birth, email,
phonenumber, password) VALUES
('John Doe', 'Male', '1985-04-12', 'john.doe@example.com', 1234567890, 1234),
('Jane Smith', 'Female', '1990-08-20', 'jane.smith@example.com',
987654321, 5678),
('Ali Khan', 'Male', '2000-11-15', 'ali.khan@example.com', 555111222, 7890),
('Sara Ali', 'Female', '1995-07-10', 'sara.ali@example.com', 444555666, 2345),
('Omar Farooq', 'Male', '1988-03-05', 'omar.farooq@example.com',
333222111, 6789);
GO


INSERT INTO [Ophthalmologist] (name, email, phonenumber, clinicname,
clinicaddress, password) VALUES
('Dr. Sarah Smith', 'dr.sarah@example.com', 555123456, 'Eye Care
Clinic', '1234 Main St, City', 5555),
('Dr. Imran Qureshi', 'dr.imran@example.com', 555987654, 'Vision
Center', '5678 Elm St, City', 7777),
('Dr. Ayesha Khan', 'dr.ayesha@example.com', 555111333, 'Vision Plus',
'9101 Oak St, City', 8888),
('Dr. Ali Raza', 'dr.ali@example.com', 555444555, 'Eye Health Clinic',
'1213 Pine St, City', 9999),
('Dr. Sana Iqbal', 'dr.sana@example.com', 555666777, 'Clear Vision',
'1415 Maple St, City', 1111);
GO


INSERT INTO [Appointment] (patient_id, ophthalmologist_id,
appointment_date, appointment_time, appointment_status) VALUES
(1,1,'2025-12-01','2025-12-01 10:00:00',1),
(2,2,'2025-12-02','2025-12-02 11:00:00',1),
(3,3,'2025-12-03','2025-12-03 12:00:00',1),
(4,4,'2025-12-04','2025-12-04 13:00:00',1),
(5,5,'2025-12-05','2025-12-05 14:00:00',1);
GO


INSERT INTO [Patient_Record] (patient_id, ophthalmologist_id,
appointment_id, record_date, diagnosis, prescription,
treatment_details) VALUES
(1,1,1,'2025-12-01','Cataract','Eye drops','Patient needs surgery in 2 weeks'),
(2,2,2,'2025-12-02','Glaucoma','Medication','Follow up in 1 month'),
(3,3,3,'2025-12-03','Myopia','Glasses','Check vision every 6 months'),
(4,4,4,'2025-12-04','Astigmatism','Contact lenses','Annual checkup
recommended'),
(5,5,5,'2025-12-05','Dry Eyes','Eye drops','Use artificial tears twice daily');
GO


INSERT INTO [Bill] (patient_id, appointment_id, amount,
payment_status, payment_date) VALUES
(1,1,5000,1,'2025-12-01'),
(2,2,7000,0,'2025-12-02'),
(3,3,3000,1,'2025-12-03'),
(4,4,4000,1,'2025-12-04'),
(5,5,3500,0,'2025-12-05');
GO


INSERT INTO [Feedback] (patient_id, ophthalmologist_id, rating,
comments, feedback_date) VALUES
(1,1,5,'Excellent care','2025-12-01'),
(2,2,4,'Good service','2025-12-02'),
(3,3,5,'Very professional','2025-12-03'),
(4,4,4,'Helpful and kind','2025-12-04'),
(5,5,5,'Highly recommended','2025-12-05');
GO

INSERT INTO [Notification] (appointment_id, recipient_id,
recipient_type, sent_date, message, message_read) VALUES
(1,1,'Patient','2025-11-28','Your appointment is scheduled for
2025-12-01 at 10:00',0),
(2,2,'Patient','2025-11-28','Your appointment is scheduled for
2025-12-02 at 11:00',0),
(3,3,'Patient','2025-11-28','Your appointment is scheduled for
2025-12-03 at 12:00',0),
(4,4,'Patient','2025-11-28','Your appointment is scheduled for
2025-12-04 at 13:00',0),
(5,5,'Patient','2025-11-28','Your appointment is scheduled for
2025-12-05 at 14:00',0);
GO
