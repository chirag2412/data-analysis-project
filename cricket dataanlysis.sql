use resume_chelleng_10;
SELECT * FROM dim_match_summary;
SELECT * FROM dim_players;
SELECT * FROM fact_bating_summary;
SELECT * FROM fact_bowling_summary;
#1Top 10 batsmen based on past 3 years total runs scored.
select x.batsmanName, sum(x.runs) as total_runs  from 
(select f.batsmanName, f.runs ,d.team1,d.team2,d.winner from dim_match_summary d join fact_bating_summary f on d.match_id=f.match_id) x
group by x.batsmanname order by total_runs  desc limit 10;

 #2Top 10 batsmen based on past 3 years average batting (min 60 balls faced in eachseason)
 select batsmanName,sum(balls) as total_balss,count(batsmanName) as numberof_matchpalyed,sum(runs) as total_runs,sum(runs)/count(batsmanName) average_batting 
 from  fact_bating_summary 
  group by batsmanname having total_balss>=60 order by average_batting desc limit 10;
 
 #Top 10 batsmen based on past 3 years strike rate (min 60 balls faced in each season)
select x.batsmanName, avg(x.sr) as avg_sr,sum(balls) as total_balss from (select f.batsmanName, f.sr ,f.balls,d.team1,d.team2,d.winner 
from dim_match_summary d join fact_bating_summary f on d.match_id=f.match_id) x
 group by x.batsmanName having total_balss>60 order by avg_sr desc limit 10;
 
 select bowlerName,sum(wickets) as total_wickets from fact_bowling_summary  group by bowlername order by total_wickets desc limit 10;
 
 #Top 10 bowlers based on past 3 years economy rate. (min 60 balls bowled in each season
select bowlerName ,avg(economy) as avg_economy,sum(overs) as total_overs from fact_bowling_summary 
group by bowlername having  total_overs>10  order by avg_economy  limit 10;


#Top 5 batsmen based on past 3 years boundary %
select r.batsmanname,sum(r.boundary_) as total_boundary,(sum(r.boundary_)/(select sum(x.boundary_) 
from (select batsmanname,'4s' as boundary_type,4s as boundary_ from fact_bating_summary
union all
select batsmanname,'6s' as boundary_type,6s as boundary_ from fact_bating_summary)x))*100 as boundary_percentage 
from (select batsmanname,'4s' as boundary_type,4s as boundary_ from fact_bating_summary
union all
select batsmanname,'6s' as boundary_type,6s as boundary_ from fact_bating_summary) r 
group by r.batsmanname order by boundary_percentage desc limit 5 ;

select r.batsmanname,sum(r.boundary_) as total_boundary
from (select batsmanname,'4s' as boundary_type,4s as boundary_ from fact_bating_summary
union all
select batsmanname,'6s' as boundary_type,6s as boundary_ from fact_bating_summary) r 
group by r.batsmanname  ;
 
 #Top 10 bowlers based on past 3 years bowling average. (min 60 balls bowled in each season)
select bowlerName,count(bowlerName) as numberof_matchpalyed,sum(wickets) as total_wickets,sum(wickets)/count(bowlerName) average_bowling,sum(overs) as total_overs 
from  fact_bowling_summary    
group by bowlername having  total_overs>10  order by average_bowling desc limit 10;

#Top 5 bowlers based on past 3 years dot ball %.
select sum(0s) from fact_bowling_summary;
select bowlerName ,sum(0s) as total_dotball,sum(overs) as total_overs,
(sum(0s)/(select sum(0s) from fact_bowling_summary))*100 as dotball_percentage from fact_bowling_summary 
group by bowlername having  total_overs>10  order by dotball_percentage desc limit 5;

#Top 4 teams based on past 3 years winning %.

select winner ,count(winner) as total_win  from dim_match_summary  group by winner order by total_win desc limit 4;

#Top 2 teams with the highest number of wins achieved by chasing targets over the past 3 years.
select winner ,count(winner) as total_win  from dim_match_summary  
 where margin like '%wickets%' group by winner order by total_win desc limit 2 ;