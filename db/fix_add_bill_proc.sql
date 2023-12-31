USE [Telemarketing_Center_DB]
GO
/****** Object:  StoredProcedure [dbo].[add_bill]    Script Date: 6/20/2023 10:52:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER procedure [dbo].[add_bill]
 (@Date_ datetime, @Amount_ float,  @Number_ int,  @Sent_to_ int) AS
begin
	declare @s_id int
	declare @s_add int
	
	if (SELECT count(Bill_id) FROM Bills) < 1
	begin
	set	@s_add = 1
    insert into Bills  (Bill_id, Date, Amount,  Number,  Sent_to ) values (@s_add, @Date_ , @Amount_ ,  @Number_ ,  @Sent_to_)
	end
	
	else
	begin
	set @s_id = (SELECT TOP 1 Bill_id FROM Bills ORDER BY Bill_id DESC)
	set @s_add = @s_id + 1
	insert into Bills  (Bill_id, Date, Amount,  Number,  Sent_to ) values (@s_add, @Date_ , @Amount_ ,  @Number_ ,  @Sent_to_)
	end
end
