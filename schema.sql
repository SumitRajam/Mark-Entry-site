create database sunbeam;
use sunbeam;
show tables;

CREATE TABLE courses (
  course_id int NOT NULL AUTO_INCREMENT,
  course_name varchar(255) DEFAULT NULL,
  description text DEFAULT NULL,
  PRIMARY KEY (course_id)
);

CREATE TABLE subjects (
  subject_id int NOT NULL AUTO_INCREMENT,
  subject_name varchar(255) DEFAULT NULL,
  course_id int DEFAULT NULL,
  PRIMARY KEY (subject_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE course_groups (
  group_id int NOT NULL AUTO_INCREMENT,
  group_name varchar(255) DEFAULT NULL,
  course_id int DEFAULT NULL,
  PRIMARY KEY (group_id),
  FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE evaluation_scheme (
  scheme_id int NOT NULL AUTO_INCREMENT,
  theory_weightage int DEFAULT NULL,
  lab_weightage int DEFAULT NULL,
  ial_weightage int DEFAULT NULL,
  ia2_weightage int DEFAULT NULL,
  subject_id int DEFAULT NULL,
  PRIMARY KEY (scheme_id),
  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE TABLE students (
  student_id int NOT NULL AUTO_INCREMENT,
  roll_number int DEFAULT NULL,
  student_name varchar(255) DEFAULT NULL,
  course_id int DEFAULT NULL,
  group_id int DEFAULT NULL,
  email varchar(255) DEFAULT NULL,
  password varchar(255) DEFAULT NULL,
  role varchar(255) DEFAULT 'student',
  PRIMARY KEY (student_id),
  KEY idx_course_id (course_id),
  KEY idx_group_id (group_id)
);
desc students;

CREATE TABLE staff (
  staff_id int NOT NULL AUTO_INCREMENT,
  employee_number int DEFAULT NULL,
  staff_name varchar(255) DEFAULT NULL,
  email varchar(255) DEFAULT NULL,
  password varchar(255) DEFAULT NULL,
  role enum('staff', 'coordinator', 'admin') DEFAULT 'staff',
  course_name varchar(255) default 'DAC',
  PRIMARY KEY (staff_id)
);
CREATE TABLE marksentry (
  entry_id int NOT NULL AUTO_INCREMENT,
  student_id int DEFAULT NULL,
  subject_id int DEFAULT NULL,
  group_id int DEFAULT NULL,
  course_id int DEFAULT NULL,
  staff_id int DEFAULT NULL,
  theory int DEFAULT NULL,
  lab int DEFAULT NULL,
  IA1 int DEFAULT NULL,
  IA2 int DEFAULT NULL,
  from_date date DEFAULT NULL,
  till_date date DEFAULT NULL,
  approved tinyint(1) DEFAULT 0,
  PRIMARY KEY (entry_id),
  foreign key (student_id) references students(student_id),
  foreign key (subject_id) references subjects(subject_id),
  foreign key (group_id) references course_groups(group_id),
  foreign key (course_id) references courses(course_id),
  foreign key (staff_id) references staff(staff_id)
);
desc marksentry;
