--Триггер для оплаты

use Telemarketing_Center_DB;
go
create trigger paymant
on Bills
after insert
as
declare @howmuch float
select @howmuch = Bills.Amount from Bills where Bill_id = (select Bill_id from inserted)
declare @Taker int
select @Taker = Bills.Sent_to from Bills where Bill_id = (select Bill_id from inserted)
update Details set Balance = Balance - @howmuch where Details.Number = (select Number from inserted)
update Details set Balance = Balance + @howmuch where Details.Number = @Taker



--Процедура для заполения опросов

use Telemarketing_Center_DB;
go
create procedure surveys_insert (@Name varchar(10), @Email varchar(20), @Deal_ varchar(500), @t_deal varchar(25), @sugg varchar(500), @Date_ datetime) AS
begin
	declare @id_ int 
	declare @s_id int
	declare @s_add int
	declare @check int
	set @id_ = (select Customers.CustomerID from Customers where Customers.Email = @Email and Customers.First_Name = @Name)
	if @id_ is not NULL
		if (SELECT COUNT(Surveys.SurveysID) FROM Surveys where Surveys.CustomerID = @id_ and (Surveys.Date is NULL) or (Surveys.Type_of_deal is NULL) or (Surveys.Deal is NULL) or (Surveys.Suggestions is NULL)) = 0
			begin
				set @s_id = (SELECT TOP 1 Surveys.SurveysID FROM Surveys ORDER BY SurveysID DESC)
				set @s_add = @s_id + 1
				insert into Surveys (SurveysID,CustomerID,Surveys.Date,Type_of_deal,Deal,Suggestions) values (@s_add, @id_, @Date_ , @t_deal, @Deal_,@sugg)
				set @check = 0 
				return @check
			end
		ELSE
			begin
			update Surveys set Surveys.Date = @Date_, Type_of_deal = @t_deal, Deal = @Deal_, Suggestions = @sugg where Surveys.CustomerID = @id_
			set @check = 0 
			return @check
			end
	else
		set @check = 1 
		return @check
End





--Процедура выбора всех опросов

use Telemarketing_Center_DB;
go
create procedure select_surveys as
begin
select * from Surveys
end






--Процедура добавления чека

use Telemarketing_Center_DB;
go
create procedure add_bill
 (@Date_ datetime, @Amount_ float,  @Number_ int,  @Sent_to_ int) AS
begin
	declare @s_id int
	declare @s_add int
	
	set @s_id = (SELECT TOP 1 Bill_id FROM Bills ORDER BY Bill_id DESC)
	set @s_add = @s_id + 1

	insert into Bills  (Bill_id, Date, Amount,  Number,  Sent_to ) values (@s_add, @Date_ , @Amount_ ,  @Number_ ,  @Sent_to_)
end





--Процедура сортировки опросов

use Telemarketing_Center_DB;
go
create procedure sort_surveys(@table_name varchar(15)) AS
begin
	DECLARE @SQL NVARCHAR(MAX)
	if (SELECT count(*) FROM information_schema.COLUMNS WHERE COLUMN_NAME = @table_name) <> 0
		begin
			SET @SQL = N'SELECT * FROM Surveys ORDER BY ' + QUOTENAME(@table_name)
			EXEC sp_executesql @SQL
			return 0
		end
	else
		return 1
end




--Процедура добавления новостей

use Telemarketing_Center_DB
go
create procedure add_news(@new varchar(100), @id int) as
begin
	declare @s_id int
	declare @s_add int
	declare @check int
	set @s_id = (SELECT TOP 1 NewID FROM Bank_News ORDER BY NewID DESC)
	set @s_add = @s_id + 1
	if @id in (select Customers.AccountID from Customers)
		begin
			insert into Bank_News (NewID,New,AccountID) values (@s_add, @new,@id)
			set @check = 0
			return @check
		end
	else
		set @check = 1
		return @check
end



--Триггер проверки уникальности новости


use Telemarketing_Center_DB;
go
create trigger check_unical_new
on Bank_News
after insert
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Bank_News c
        INNER JOIN INSERTED i ON c.New = i.New
        GROUP BY c.New
        HAVING COUNT(*) > 1
    )
    BEGIN
        RAISERROR ('Duplicate email address found.', 16, 1);
        ROLLBACK TRANSACTION; -- Optionally, rollback the transaction to prevent the duplicate data from being inserted or updated.
    END;
END;



--Процедура выбора новости

use Telemarketing_Center_DB;
go
create procedure select_news(@colum_ NVARCHAR(15))
as
begin
declare @check int
if @colum_ = ''
	begin
		select * from Bank_News
		set @check = 0
		return @check
	end
else
	if @colum_ = 'New'
	begin
		select * from Bank_News order by New
		set @check = 0
		return @check
	end
	else
		if @colum_ = 'AccountID'
		begin
		select * from Bank_News order by AccountID
		set @check = 0
		return @check
		end
		else
			set @check = 1
			return @check 
end





use Telemarketing_Center_DB;
go
create procedure select_news(@colum_ NVARCHAR(15))
as
begin
declare @check int
if @colum_ = ''
	begin
		select * from Bank_News
	end
else
	if @colum_ = 'New'
	begin
		select * from Bank_News order by New
	end
	else
		if @colum_ = 'AccountID'
		begin
		select * from Bank_News order by AccountID
		end
		else
			set @check = -1
			return @check 
end


--Процедура добавления сообщения

use Telemarketing_Center_DB;
go
create procedure add_messages(@mess varchar(500), @custID int, @leadID int) as
begin
declare @s_id int
declare @s_add int
declare @date_ datetime
declare @status varchar(10)
if (SELECT count(MessageID) FROM Messages ) < 1
	begin
		set	@s_id = 3000
		set @date_ = GETDATE()
		set @status = 'await'
		insert into Messages(MessageID,Text,CustomerID,LeadID,Date,Status) values (@s_id,@mess,@custID,@leadID,@date_ ,@status)
	end
else
	begin
	set @s_id = (SELECT TOP 1 Messages.MessageID FROM Messages ORDER BY MessageID DESC)
	set @s_add = @s_id + 1
	set @date_ = GETDATE()
	set @status = 'await'
	insert into Messages(MessageID,Text,CustomerID,LeadID,Date,Status) values (@s_add,@mess,@custID,@leadID,@date_,@status)
	end
end


exec add_messages @mess = 'test mess two', @custID = 2, @leadID = NULL





--Триггер проверки уникальности сообщения

use Telemarketing_Center_DB;
go
create trigger check_unical_mess
on Messages
after insert
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Messages c
        INNER JOIN INSERTED i ON c.Text = i.Text
        GROUP BY c.Text
        HAVING COUNT(*) > 1
    )
    BEGIN
        RAISERROR ('Duplicate message found.', 16, -- Severity 
												1 -- State
												);
        ROLLBACK TRANSACTION; -- Optionally, rollback the transaction to prevent the duplicate data from being inserted or updated.
    END;
END;




--Процедура обновления информации о лидах



use Telemarketing_Center_DB
go
CREATE PROCEDURE UpdateLeadInformation
(@lead_id int, @Phone varchar(11), @Email varchar(20),
	@Lead_note varchar(1000), @First_Name varchar(10), 
	@Last_Name varchar(10), @Father_Name varchar(10), 
	@sex varchar(1))
as
BEGIN
    UPDATE Leads
    SET Phone = @Phone,
		Email = @Email,
		Lead_note = @Lead_note,
		First_Name = @First_Name,
        Last_Name = @Last_Name,
		Father_Name = @Father_Name,
		Sex = @sex
    WHERE LeadID = @lead_id
END




Процедура добавления лида 

use Telemarketing_Center_DB
go
CREATE PROCEDURE AddLeadProcedure
 (@lead_id int, @Phone varchar(11), @Email varchar(20),
	@Lead_note varchar(1000), @First_Name varchar(10), 
	@Last_Name varchar(10), @Father_Name varchar(10), 
	@gender varchar(1))
as
BEGIN
declare @id int
declare @add int
if (SELECT count(LeadID) FROM Leads) < 1
begin
	set	@id = 5000
    INSERT INTO Leads (LeadID,Phone,Email,Lead_note,First_Name,Last_Name,Father_Name,Sex) 
	VALUES (@id,@Phone,@Email,@Lead_note,@First_Name,@Last_Name,@Father_Name, @gender)
end
else
	begin
	set @id = (SELECT TOP 1 Leads.LeadID FROM Leads ORDER BY LeadID DESC)
	set @add = @id + 1
	INSERT INTO Leads (LeadID,Phone,Email,Lead_note,First_Name,Last_Name,Father_Name,Sex) 
	VALUES (@add,@Phone,@Email,@Lead_note,@First_Name,@Last_Name,@Father_Name, @gender)
	end
END



--Триггер на уникальность емайла




create trigger check_unical_mail
on Customers
after insert,update
AS
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Customers c
        INNER JOIN INSERTED i ON c.Email = i.Email
        GROUP BY c.Email
        HAVING COUNT(*) > 1
    )
    BEGIN
        RAISERROR ('Duplicate email found.', 16, -- Severity 
												1 -- State
												);
        ROLLBACK TRANSACTION; -- Optionally, rollback the transaction to prevent the duplicate data from being inserted or updated.
    END;
END;



update Customers set Email = 'example@example.com' where AccountID = 3




--Сделать триггер насчитывающий бюджет компании КОНСТАНТА + СТОИМОСТЬ ПРОДУКТА ИЛИ ПРОДУКТОВ 

CREATE TRIGGER UpdateCompanyBudgetTrigger
ON Products
AFTER INSERT, UPDATE
AS
BEGIN
    -- Set the constant budget value
    DECLARE @constantBudget float= 100000.00 -- Adjust this value as needed

    -- Calculate the total cost of directly involved products for the company
    DECLARE @companyId INT
    SELECT @companyId = CampaignID
    FROM Products
    WHERE CampaignID = (SELECT CampaignID FROM inserted) 

    DECLARE @totalCost float
    SELECT @totalCost = SUM(p.Cost)
    FROM Products p
    WHERE p.ProductID IN (
        SELECT ProductID
        FROM Products
        WHERE CampaignID = @companyId
    )

    UPDATE Campaigns
    SET Budget = @constantBudget + @totalCost
    WHERE CampaignID = @companyId
END

--После того как есть компания 

update Products set CampaignID = 111111





--Триггер проверяющий чтобы ID сотрудника отличались от ID клиента

use Telemarketing_Center_DB;
go
create trigger check_account_id
on Customers
after insert,update
as
begin
DECLARE @customer_id INT
SELECT @customer_id = AccountID FROM inserted

 IF EXISTS (SELECT 1 FROM inserted i INNER JOIN Employees e ON i.AccountID = e.AccountID)
	 BEGIN
        RAISERROR ('Duplicate id clietn whith id employee found.', 16, -- Severity 
																	1 -- State
																				);
        ROLLBACK TRANSACTION; -- Optionally, rollback the transaction to prevent the duplicate data from being inserted or updated.
    END;

end


update Customers set AccountID = 1 where CustomerID = 3

exec add_customers @first_name = 'test',@last_name = 'тест',@father_name = 'тестович',@date_of_bith = '2001-01-01',@preference = 'eat',@email = 'test@test.com',@phone = '11111111',@sex = 'M',@acc_id = 1


--Процедура добавления клиентов


use Telemarketing_Center_DB
go
create procedure add_customers (@first_name varchar(10),@last_name varchar(10),@father_name varchar(10),@date_of_bith date,@preference varchar(50),@email varchar(20),@phone varchar(11),@sex varchar(1),@acc_id int)
as
begin
declare @id int
declare @add int
if (SELECT count(CustomerID) FROM Customers) < 1
begin
	set	@id = 1
    INSERT INTO Customers(CustomerID,First_Name,Last_Name,Father_Name,Date_of_Birth,Preferences,Email,Phone,Sex,AccountID) 
	VALUES (@id,@first_name,@last_name,@father_name,@date_of_bith,@preference,@email,@phone,@sex,@acc_id )
end
else
	begin
	set @id = (SELECT TOP 1 Customers.CustomerID FROM Customers ORDER BY CustomerID DESC)
	set @add = @id + 1
	INSERT INTO Customers(CustomerID,First_Name,Last_Name,Father_Name,Date_of_Birth,Preferences,Email,Phone,Sex,AccountID) 
	VALUES (@add,@first_name,@last_name,@father_name,@date_of_bith,@preference,@email,@phone,@sex,@acc_id )
	end
end




--Процедура добавления продукта

use Telemarketing_Center_DB
go
create procedure add_product(@product_name varchar(15),@product_description varchar(100),@product_type varchar(50),@product_interest varchar(10),@cost float)
as
BEGIN
declare @id int
declare @add int
declare @campId int 
set @campId = NULL
if (SELECT count(ProductID) FROM [Products]) < 1
begin
	set	@id = 9999
	
    INSERT INTO Products (ProductID,Product_Name,Product_Descript,Product_Type,Product_interest,CampaignID,Cost) 
	VALUES (@id,@product_name,@product_description,@product_type,@product_interest,@campId,@cost)
end
else
	begin
	set @id = (SELECT TOP 1 Leads.LeadID FROM Leads ORDER BY LeadID DESC)
	set @add = @id + 1
	INSERT INTO Products (ProductID,Product_Name,Product_Descript,Product_Type,Product_interest,CampaignID,Cost) 
	VALUES (@add,@product_name,@product_description,@product_type,@product_interest,@campId,@cost)
	end
END




exec add_product @product_name = 'Product_test',@product_description = 'description_test',@product_type = 'Type_test',@product_interest = 'product_interest',@cost=1000



--Процедура добавления компании
use Telemarketing_Center_DB
go
create procedure add_camp(@status varchar(5), @employeeID int)
as
begin
declare @id int
declare @add int
if (SELECT count(CampaignID) FROM Campaigns) < 1
begin
	set	@id = 111111
    INSERT INTO Campaigns(CampaignID,Campaign_status,EmployeeID) 
	VALUES (@id,@status,@employeeID)
end
else
	begin
	set @id = (SELECT TOP 1 Campaigns.CampaignID FROM Campaigns ORDER BY CampaignID DESC)
	set @add = @id + 1
	INSERT INTO Campaigns(CampaignID,Campaign_status,EmployeeID) 
	VALUES (@add,@status,@employeeID)
	end

end




exec add_camp @status = 'start', @employeeID = 1









--Триггер контроля статуса компании
use Telemarketing_Center_DB
go
create trigger check_status_camp
on Campaigns
after insert,update
as
begin
DECLARE @campaign_id INT
if (select Campaign_status from inserted) = 'start'
	begin
		SELECT @campaign_id = CampaignID
		FROM inserted

		UPDATE Campaigns SET Campaign_start = GETDATE() WHERE CampaignID = @campaign_id
	end
else 
	begin
		if (select Campaign_status from inserted) = 'end'
		begin
		SELECT @campaign_id = CampaignID
		FROM inserted
		UPDATE Campaigns SET Campaign_end = GETDATE() WHERE CampaignID = @campaign_id
		end
		else
			begin
				UPDATE Campaigns SET Campaign_end = NULL WHERE CampaignID = @campaign_id
			end
	end
end





update Campaigns set Campaign_status = 'end' where CampaignID = 111111

