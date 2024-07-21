use psyliq;
#1.Select all female patients who are older than 40.
select EmployeeName,age,gender from diabetes_prediction where gender='Female' and age>40;

#2.Calculate the average BMI of patients.
select avg(bmi)  from diabetes_prediction ;
#Retrieve the Patient_ids of patients who have a BMI greater than the average BMI
select Patient_id from diabetes_prediction where bmi>(select avg(bmi) from diabetes_prediction);

#3.Find the patient with the highest HbA1c level and the patient with the lowest HbA1clevel.
select EmployeeName,HbA1c_level
from diabetes_prediction
 where HbA1c_level=(select max(HbA1c_level) from diabetes_prediction) or HbA1c_level=(select min(HbA1c_level) from diabetes_prediction)order by HbA1c_level desc;
 


#4.List patients in descending order of blood glucose levels.
select EmployeeName from diabetes_prediction order by blood_glucose_level desc;

#5.Find patients who have hypertension and diabetes.
select EmployeeName from diabetes_prediction where hypertension=1 and diabetes=1;

#6.Determine the number of patients with heart disease
select count(heart_disease) from diabetes_prediction where heart_disease=1;

#7.Group patients by smoking history and count how many smokers and nonsmokers there are
select smoking_history,count(smoking_history) from diabetes_prediction group by smoking_history;

#8.Rank patients by blood glucose level within each gender group\\
select EmployeeName,gender,blood_glucose_level,rank()over(partition by gender order by blood_glucose_level desc) as eemployee_rank from diabetes_prediction order by eemployee_rank asc;`2014`
select EmployeeName,gender,blood_glucose_level,dense_rank()over(partition by gender order by blood_glucose_level desc) as eemployee_rank from diabetes_prediction order by eemployee_rank asc;
#if there's ties or same number the next rank will not skipp in dense rank but in rank
#over specifies the set of row that window function operate
#20,20,10,10,5
#for  rank-1,1,3,3,5-leaves gaps between ranks after tie  denserank-1,1,2,2,3-leaves  no gaps between ranks after tie
#9.Find patients who have hypertension but not diabetes using the EXCEPT operator
select * from diabetes_prediction;
alter table diabetes_prediction
add constraint Patient_id unique(Patient_id(15));
SELECT * FROM psyliq.diabetes_prediction;
#10.Update the smoking history of patients who are older than 50 to "Ex-smoker."
set sql_safe_updates=0;
update diabetes_prediction
set smoking_history='EX-smoker'
where age>50; 
SELECT smoking_history,age FROM psyliq.diabetes_prediction where age>50;

# 11.Insert a new patient into the database with sample data.
insert into diabetes_prediction(EmployeeName, Patient_id, gender, age, hypertension, heart_disease, smoking_history, bmi, HbA1c_level, blood_glucose_level, diabetes)
values('mic','pt100045','male',57,1,1,'former',5.6,4.7,150,1);
SELECT EmployeeName,smoking_history,age FROM psyliq.diabetes_prediction where EmployeeName='mic';

#12.Delete all patients with heart disease from the database.
delete from diabetes_prediction 
where heart_disease=1;
